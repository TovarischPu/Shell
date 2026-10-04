import tkinter as tk
from tkinter import scrolledtext
import shlex
import sys
import argparse

class VFSShell:
    def __init__(self, root, vfs_path=None, script_path=None):
        self.root = root
        self.root.title("VFS Shell Emulator")
        self.root.geometry("700x450")
        self.root.configure(bg="#1e1e1e")

        self.output = scrolledtext.ScrolledText(
            root, bg="#1e1e1e", 
            fg="#00ff00", 
            font=("Menlo", 13), 
            insertbackground="white", 
            relief=tk.FLAT, borderwidth=0)
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output.config(state=tk.DISABLED)

        self.input_frame = tk.Frame(root, bg="#1e1e1e")
        self.input_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.prompt = tk.Label(
            self.input_frame, text="vfs $ ", font=("Menlo", 13), 
            bg="#1e1e1e", fg="#00aaff")
        self.prompt.pack(side=tk.LEFT)
        self.entry = tk.Entry(
            self.input_frame, 
            bg="#1e1e1e", 
            fg="#ffffff", 
            font=("Menlo", 13), 
            insertbackground="white", 
            relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.process_input)
        self.entry.focus()
        self.print_to_output("Welcome to VFS Shell. Type 'exit' to quit.\n\n")
        self._print_debug_info(vfs_path, script_path)
        if script_path:
            self._execute_startup_script(script_path)

    def _print_debug_info(self, vfs_path, script_path):
        self.print_to_output("--- Debug: Startup Parameters ---\n")
        
        vfs_str = vfs_path if vfs_path else "Not specified"
        script_str = script_path if script_path else "Not specified"
        
        self.print_to_output(f"VFS Path:   {vfs_str}\n")
        self.print_to_output(f"Script Path: {script_str}\n")
        self.print_to_output("-----------------------------\n\n")

    def _execute_startup_script(self, script_path):
        header = f"--- Executing script: {script_path} ---\n"
        self.print_to_output(header)
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                for line in f:
                    cmd = line.strip()
                    if not cmd or cmd.startswith('#'):
                        continue
                    if cmd == "exit":
                        self.print_to_output(
                            "Skipping 'exit' in script.\n"
                        )
                        continue
                    self.print_to_output(f"vfs $ {cmd}\n")
                    try:
                        self.run_command(cmd)
                    except Exception as err:
                        err_msg = f"Error executing '{cmd}': {err}\n"
                        self.print_to_output(err_msg)

            self.print_to_output("--- Script finished ---\n\n")
        except FileNotFoundError:
            msg = f"Error: script not found: {script_path}\n\n"
            self.print_to_output(msg)
        except Exception as err:
            self.print_to_output(
                f"Error reading script: {err}\n\n"
            )
    def print_to_output(self, text):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)
    def process_input(self,event=None):
        user_input=self.entry.get()
        self.entry.delete(0, tk.END)
        self.print_to_output(f"vfs $ {user_input}\n")
        
        if not user_input.strip():
            return
        self.run_command(user_input)
    def run_command(self, user_input):
        try:
            args=shlex.split(user_input)
        except ValueError as e:
            self.print_to_output(f"Error: unmatched quotes in input. ({e})\n")
            return
        command=args[0]
        c1=args[1:]

        if command=="exit":
            self.print_to_output("Exiting VFS Shell...\n")
            self.root.destroy()
            sys.exit(0)
            
        elif command=="ls":
            self.print_to_output(f"Command 'ls' executed with args: {c1}\n")
            
        elif command=="cd":
            self.print_to_output(f"Command 'cd' executed with args: {c1}\n")
            
        else:
            self.print_to_output(f"Error: command not found: {command}\n")
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="VFS Shell Emulator"
    )
    parser.add_argument(
        "--vfs-path", 
        help="Path to the physical location of the VFS"
    )
    parser.add_argument(
        "--script", 
        help="Path to the startup script to execute"
    )
    return parser.parse_args()
if __name__=="__main__":
    args = parse_arguments()
    root = tk.Tk()
    app = VFSShell(root, vfs_path=args.vfs_path, script_path=args.script)
    root.mainloop()