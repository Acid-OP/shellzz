# builtin_commands.py
import os
import getpass
import socket
from datetime import datetime
import curses
from .colors import *
from .display import clear_and_setup, show_ascii_art

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
    elif cmd == curses.KEY_PPAGE:
        print("hello")
        return True
    
    return False
