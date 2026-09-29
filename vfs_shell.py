import tkinter as tk
from tkinter import scrolledtext
import shlex
import sys

class VFSShell:
    def __init__(self, root):
        self.root = root

        self.root.title("VFS Shell Emulator")
        self.root.geometry("700x450")
        self.root.configure(bg="#1e1e1e")

        # Поле вывода
        self.output = scrolledtext.ScrolledText(
            root, bg="#1e1e1e", fg="#00ff00", font=("Menlo", 13), 
            insertbackground="white", relief=tk.FLAT, borderwidth=0
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output.config(state=tk.DISABLED)

        # Поле ввода
        self.input_frame = tk.Frame(root, bg="#1e1e1e")
        self.input_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.prompt = tk.Label(
            self.input_frame, text="vfs $ ", font=("Menlo", 13), 
            bg="#1e1e1e", fg="#00aaff"
        )
        self.prompt.pack(side=tk.LEFT)

        self.entry = tk.Entry(
            self.input_frame, bg="#1e1e1e", fg="#ffffff", 
            font=("Menlo", 13), insertbackground="white", relief=tk.FLAT
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.process_input)
        self.entry.focus()

        self.print_to_output("Welcome to VFS Shell. Type 'exit' to quit.\n\n")

    def print_to_output(self, text):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def process_input(self, event=None):
        user_input = self.entry.get()
        self.entry.delete(0, tk.END)
        self.print_to_output(f"vfs $ {user_input}\n")

        if not user_input.strip():
            return
        try:
            args = shlex.split(user_input)
        except ValueError as e:
            self.print_to_output(f"Error: unmatched quotes in input. ({e})\n")
            return
        command = args[0]
        cmd_args = args[1:]

        if command == "exit":
            self.print_to_output("Exiting VFS Shell...\n")
            self.root.destroy()
            sys.exit(0)
            
        elif command == "ls":
            self.print_to_output(f"Command 'ls' executed with args: {cmd_args}\n")
            
        elif command == "cd":
            self.print_to_output(f"Command 'cd' executed with args: {cmd_args}\n")
            
        else:
            self.print_to_output(f"Error: command not found: {command}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = VFSShell(root)
    root.mainloop()