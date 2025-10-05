# external_commands.py
import subprocess
from colors import *

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
