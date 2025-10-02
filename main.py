# main.py
from .display import clear_and_setup, get_colored_prompt
from .builtin_commands import handle_builtin_commands
from .external_commands import run_external_command
from .colors import *

def main():
    clear_and_setup()
    
    while True:
        try:
            prompt = get_colored_prompt()
            line = input(prompt).strip()
            
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
