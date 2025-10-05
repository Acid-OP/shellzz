import re
import subprocess
from pathlib import Path
from colors import *

class LLMFileGenerator:
    """Handles parsing LLM responses and generating real files"""
    
    def __init__(self):
        self.last_files = []
        self.last_commands = []
    
    def parse_response(self, response_text):
        """
        Parse LLM response for file generation instructions.
        Looks for XML tags like:
        <file path="src/app.js">content</file>
        <command>npm install</command>
        """
        files = []
        commands = [] 
        
        file_pattern = r'<file path="([^"]+)">\s*(.*?)\s*</file>'
        for match in re.finditer(file_pattern, response_text, re.DOTALL):
            path = match.group(1).strip()
            content = match.group(2)
            files.append({'path': path, 'content': content})
        
        command_pattern = r'<command>(.*?)</command>'
        for match in re.finditer(command_pattern, response_text, re.DOTALL):
            commands.append(match.group(1).strip())
        
        self.last_files = files
        self.last_commands = commands
        
        return files, commands
    
    def has_file_instructions(self, response_text):
        """Check if response contains file generation instructions"""
        return '<file path=' in response_text or '<command>' in response_text
    
    def create_files(self, files, base_dir="."):
        """Create actual files on disk"""
        created_files = []
        
        if not files:
            return created_files
        
        Path(base_dir).mkdir(parents=True, exist_ok=True)
        
        print(f"\n{CYAN}📁 Creating {len(files)} file(s)...{RESET}")
        
        for file_info in files:
            try:
                file_path = Path(base_dir) / file_info['path']
                
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_info['content'])
                
                created_files.append(str(file_path))
                print(f"{GREEN}✓ Created: {file_path}{RESET}")
                
            except Exception as e:
                print(f"{RED}✗ Failed to create {file_info['path']}: {e}{RESET}")
        
        return created_files
    
    def run_commands(self, commands, cwd="."):
        """Execute commands in the specified directory"""
        if not commands:
            return []
        
        print(f"\n{YELLOW}⚙️  Running {len(commands)} command(s)...{RESET}")
        results = []
        
        for cmd in commands:
            print(f"\n{CYAN}→ Running: {BOLD}{cmd}{RESET}")
            
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    timeout=300 
                )
                
                if result.returncode == 0:
                    print(f"{GREEN}✓ Success{RESET}")
                    if result.stdout.strip():
                        print(result.stdout)
                    results.append({
                        'command': cmd,
                        'success': True,
                        'output': result.stdout
                    })
                else:
                    print(f"{RED}✗ Failed with code {result.returncode}{RESET}")
                    if result.stderr:
                        print(f"{RED}{result.stderr}{RESET}")
                    results.append({
                        'command': cmd,
                        'success': False,
                        'error': result.stderr
                    })
                    
            except subprocess.TimeoutExpired:
                print(f"{RED}✗ Command timed out (5 min limit){RESET}")
                results.append({
                    'command': cmd,
                    'success': False,
                    'error': 'Timeout'
                })
            except Exception as e:
                print(f"{RED}✗ Error: {e}{RESET}")
                results.append({
                    'command': cmd,
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    def process_response(self, response_text, project_dir="."):
        """
        Main method: parse response and generate files/run commands
        Returns True if files were generated, False otherwise
        """
        if not self.has_file_instructions(response_text):
            return False
        
        files, commands = self.parse_response(response_text)
        
        if not files and not commands:
            return False
        
        created_files = self.create_files(files, base_dir=project_dir)
        
        if commands:
            results = self.run_commands(commands, cwd=project_dir)
            
            failed = [r for r in results if not r['success']]
            if failed:
                print(f"\n{YELLOW}⚠️  {len(failed)} command(s) failed{RESET}")
        
        if created_files:
            print(f"\n{GREEN}✅ Generated {len(created_files)} file(s) in '{project_dir}/'{RESET}")
            print(f"{CYAN}📂 Files created:{RESET}")
            for f in created_files:
                print(f"   {GREEN}- {f}{RESET}")
        
        return True
    
    def get_enhanced_prompt(self):
        """
        Returns a system prompt addition to teach Gemini how to generate files.
        Add this to your Gemini system instructions.
        """
        return """
            When the user asks you to create, generate, or build files or a project, respond with file generation instructions using this XML format:
            <file path="relative/path/to/file.ext">
            FILE_CONTENT_HERE
            </file>

            <command>command to run after files are created</command>

            Example:
            <file path="src/server.js">
            const express = require('express');
            const app = express();

            app.get('/hello', (req, res) => {
            res.json({ message: 'Hello!' });
            });

            app.listen(3000);
            </file>

            <file path="package.json">
            {
            "name": "my-app",
            "version": "1.0.0",
            "dependencies": {
                "express": "^4.18.0"
            }
            }
            </file>

            <command>npm install</command>
            <command>npm start</command>

            Rules:
            - Use relative paths from project root
            - Include ALL necessary files
            - Provide complete, working code
            - Commands run in order after all files are created
            - You can still provide explanations before or after the XML tags
            """
file_generator = LLMFileGenerator()