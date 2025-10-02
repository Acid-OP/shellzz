# display.py
import os
import getpass
import socket
from datetime import datetime
from .colors import *

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
