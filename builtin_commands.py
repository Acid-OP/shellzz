import os
import getpass
import socket
from datetime import datetime
import curses
import re
from colors import *
from display import clear_and_setup, show_ascii_art
from gemini_client import ask_gemini, ask_gemini_with_file_generation

def my_ls():
    try:
        files = os.listdir('.')
        print(f"{CYAN}📁 Files and Directories:{RESET}")
        for item in sorted(files):
            if os.path.isdir(item):
                print(f"  {BLUE}{BOLD}📁 {item}/{RESET}")  
            else:
                print(f"  {GREEN}📄 {item}{RESET}") 
    except PermissionError:
        print(f"{RED}❌ Permission denied{RESET}")

def my_pwd():
    print(f"{YELLOW}📍 Current directory: {BOLD}{os.getcwd()}{RESET}")

def my_date():
    now = datetime.now()
    print(f"{MAGENTA}🕒 {now.strftime('%A, %B %d, %Y - %I:%M:%S %p')}{RESET}")

def my_whoami():
    username = getpass.getuser()
    hostname = socket.gethostname()
    print(f"{CYAN}👤 You are: {BOLD}{username}{RESET} on Acidop shell")

def my_help():
    print(f"{BOLD}{CYAN}🛠️  AcidopShell Built-in Commands:{RESET}")
    print(f"{GREEN}  ls        {RESET}- List files and directories (custom)")
    print(f"{GREEN}  pwd       {RESET}- Show current directory (custom)")
    print(f"{GREEN}  cd <dir>  {RESET}- Change directory")
    print(f"{GREEN}  date      {RESET}- Show current date and time (custom)")
    print(f"{GREEN}  whoami    {RESET}- Show current user info (custom)")
    print(f"{GREEN}  clear     {RESET}- Clear the screen")
    print(f"{GREEN}  help      {RESET}- Show this help message")
    print(f"{GREEN}  ascii     {RESET}- Show cool ASCII art")
    print(f"{GREEN}  exit      {RESET}- Exit the shell")
    print(f"{GREEN}  ai        {RESET}- Enter AI mode with Gemini 2.5 Flash")
    print(f"{GREEN}  ai gen    {RESET}- Enter AI mode with automatic file generation")
    print(f"{YELLOW}  <command> {RESET}- Run any system command")

def handle_builtin_commands(command_parts):
    cmd = command_parts[0].lower()
    
    if cmd == "ls":
        my_ls()
        return True
    elif cmd == "pwd":
        my_pwd()
        return True
    elif cmd == "cd":
        try:
            if len(command_parts) == 1:
                os.chdir(os.path.expanduser("~"))
            else:
                os.chdir(command_parts[1])
            print(f"{GREEN}✅ Changed to: {os.getcwd()}{RESET}")
        except FileNotFoundError:
            print(f"{RED}❌ Directory not found: {command_parts[1]}{RESET}")
        except PermissionError:
            print(f"{RED}❌ Permission denied{RESET}")
        return True
    elif cmd == "date":
        my_date()
        return True
    elif cmd == "whoami":
        my_whoami()
        return True
    elif cmd == "clear":
        clear_and_setup()
        return True
    elif cmd == "help":
        my_help()
        return True
    elif cmd == "ascii":
        show_ascii_art()
        return True
    elif cmd == "ai":
        if len(command_parts) > 1 and command_parts[1].lower() == "gen":
            print(f"{YELLOW}🤖 Entering AI Gen Mode (with file generation).{RESET}")
            print(f"{CYAN}💡 Tip: Ask me to 'create a Flask app' or 'build a React component'{RESET}")
            print(f"{GREEN}📍 Current directory: {os.getcwd()}{RESET}")
            print(f"{YELLOW}Type 'exit' to leave.{RESET}\n")
            
            while True:
                query = input(f"{MAGENTA}ai-gen> {RESET}").strip()
                if query.lower() in ["exit", "quit"]:
                    print(f"{YELLOW}👋 Leaving AI Gen mode.{RESET}")
                    break
                if not query:
                    continue
                
                print(f"{YELLOW}🤖 Thinking and generating...{RESET}\n")
                
                print(f"{CYAN}📁 Where should I create the files?{RESET}")
                print(f"{YELLOW}   Examples:{RESET}")
                print(f"{YELLOW}   - Press Enter (current directory){RESET}")
                print(f"{YELLOW}   - my_project (creates folder in current dir){RESET}")
                print(f"{YELLOW}   - ~/Desktop/my_app (absolute path){RESET}")
                print(f"{YELLOW}   - ../parent_folder/project (relative path){RESET}")
                project_dir = input(f"{CYAN}   Path: {RESET}").strip()
                
                if not project_dir:
                    project_dir = "."
                    print(f"{GREEN}   ✓ Using current directory: {os.getcwd()}{RESET}")
                else:
                    project_dir = os.path.expanduser(project_dir)
      
                    if not os.path.isabs(project_dir):
                        abs_path = os.path.abspath(project_dir)
                        print(f"{GREEN}   ✓ Will create in: {abs_path}{RESET}")
                    else:
                        print(f"{GREEN}   ✓ Will create in: {project_dir}{RESET}")
    
                    if not os.path.exists(project_dir):
                        confirm = input(f"{YELLOW}   Directory doesn't exist. Create it? (Y/n): {RESET}").strip().lower()
                        if confirm and confirm != 'y' and confirm != '':
                            print(f"{RED}   ✗ Cancelled{RESET}\n")
                            continue
                        try:
                            os.makedirs(project_dir, exist_ok=True)
                            print(f"{GREEN}   ✓ Created directory{RESET}")
                        except Exception as e:
                            print(f"{RED}   ✗ Failed to create directory: {e}{RESET}\n")
                            continue
                
                print() 
                response, files_generated = ask_gemini_with_file_generation(query, project_dir)
                
                clean_response = re.sub(r'<file path="[^"]+">.*?</file>', '', response, flags=re.DOTALL)
                clean_response = re.sub(r'<command>.*?</command>', '', clean_response, flags=re.DOTALL)
                clean_response = clean_response.strip()
                
                if clean_response:
                    print(f"\n{GREEN}{clean_response}{RESET}\n")
                
                if not files_generated and '<file' not in response:
                    print(f"{YELLOW}💡 Tip: Ask me to create or generate files!{RESET}\n")
        
        elif len(command_parts) == 1:
            print(f"{YELLOW}🤖 Entering AI mode. Type 'exit' to leave.{RESET}")
            print(f"{CYAN}💡 Use 'ai gen' for file generation mode{RESET}\n")
            
            while True:
                query = input(f"{CYAN}ai> {RESET}").strip()
                if query.lower() in ["exit", "quit"]:
                    print(f"{YELLOW}👋 Leaving AI mode.{RESET}")
                    break
                if not query:
                    continue
                print(f"{YELLOW}🤖 Thinking...{RESET}")
                answer = ask_gemini(query)
                print(f"{GREEN}{answer}{RESET}\n")
        else:
            query = " ".join(command_parts[1:])
            print(f"{YELLOW}🤖 Thinking...{RESET}")
            answer = ask_gemini(query)
            print(f"{GREEN}{answer}{RESET}")
        
        return True
    
    return False