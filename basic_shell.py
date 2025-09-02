import os
import subprocess
import socket
import getpass
from datetime import datetime
# Color codes
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
BOLD = '\033[1m'
RESET = '\033[0m'
BG_BLACK = '\033[40m'

def clear_and_setup():
    """Clear terminal and setup background"""
    os.system('clear')
    print(BG_BLACK, end='') 
    print(f"{CYAN}{BOLD}")
    print("    ╔═══════════════════════════════════════╗")
    print("    ║           🚀 AcidopShell 🚀           ║") 
    print("    ║         Your Custom Shell             ║")
    print("    ╚═══════════════════════════════════════╝")
    print(f"{RESET}\n")

def get_colored_prompt():
    """Create colorful prompt with current path"""
    username = getpass.getuser()
    hostname = socket.gethostname()
    current_path = os.getcwd()
    
    if len(current_path) > 25:
        current_path = "..." + current_path[-22:]
    
    return f"{GREEN}{BOLD}{username}{RESET}@{BLUE}{hostname}{RESET}:{YELLOW}{BOLD}{current_path}{RESET}> AcidopShell$ "

def my_ls():
    """Custom built-in ls function"""
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
    """Custom built-in pwd function"""
    current_dir = os.getcwd()
    print(f"{YELLOW}📍 Current directory: {BOLD}{current_dir}{RESET}")

def my_date():
    """Custom built-in date function"""
    now = datetime.now()
    print(f"{MAGENTA}🕒 {now.strftime('%A, %B %d, %Y - %I:%M:%S %p')}{RESET}")

def my_whoami():
    """Custom built-in whoami function"""
    username = getpass.getuser()
    hostname = socket.gethostname()
    print(f"{CYAN}👤 You are: {BOLD}{username}{RESET} on {BOLD}{hostname}{RESET}")

def my_help():
    """Show available commands"""
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
    print(f"{YELLOW}  <command> {RESET}- Run any system command")

def show_ascii_art():
    """Show cool ASCII art as background"""
    art = f"""{BLUE}
    ⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀
    ⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀
    ⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀
          🚀 ACIDOP SHELL - COMMAND CENTER 🚀
    {RESET}"""
    print(art)

def handle_builtin_commands(command_parts):
    """Handle our custom built-in commands"""
    cmd = command_parts[0].lower()
    
    # Built-in: ls 
    if cmd == "ls":
        my_ls()
        return True
    
    # Built-in: pwd   
    elif cmd == "pwd":
        my_pwd()
        return True
    
    # Built-in: cd
    elif cmd == "cd":
        try:
            if len(command_parts) == 1:
                # cd with no arguments goes to home
                os.chdir(os.path.expanduser("~"))
            else:
                os.chdir(command_parts[1])
            print(f"{GREEN}✅ Changed to: {os.getcwd()}{RESET}")
        except FileNotFoundError:
            print(f"{RED}❌ Directory not found: {command_parts[1]}{RESET}")
        except PermissionError:
            print(f"{RED}❌ Permission denied{RESET}")
        return True
    
    # Built-in: date
    elif cmd == "date":
        my_date()
        return True
    
    # Built-in: whoami
    elif cmd == "whoami":
        my_whoami()
        return True
    
    # Built-in: clear
    elif cmd == "clear":
        clear_and_setup()
        return True
    
    # Built-in: help
    elif cmd == "help":
        my_help()
        return True
    elif cmd == "ascii":     
        show_ascii_art()     
        return True
    return False

def run_external_command(command_parts):
    """Run external system commands"""
    try:
        result = subprocess.run(command_parts)
        if result.returncode != 0:
            print(f"{RED}⚠️  Command exited with code: {result.returncode}{RESET}")
    except FileNotFoundError:
        print(f"{RED}❌ Command not found: {command_parts[0]}{RESET}")
    except KeyboardInterrupt:
        print(f"{YELLOW}⏸️  Command interrupted{RESET}")

def main():
    clear_and_setup()
    
    while True:
        try:
            prompt = get_colored_prompt()
            line = input(prompt).strip()
            
            # Skip empty lines 
            if not line:
                continue

            if line.lower() == "exit":
                print(f"{YELLOW}👋 Goodbye from AcidopShell!{RESET}")
                break
            
            command_parts = line.split()
            
            if handle_builtin_commands(command_parts):
                continue
            
            run_external_command(command_parts)
            
        except KeyboardInterrupt:
            print(f"\n{YELLOW}💡 Use 'exit' to quit AcidopShell{RESET}")
        except EOFError:
            print(f"\n{YELLOW}👋 Goodbye from AcidopShell!{RESET}")
            break

if __name__ == "__main__":
    main()