import tkinter as tk
from tkinter import scrolledtext
import shlex
import sys
import argparse
from VFS import VFS
import platform


class VFSShell:
    VFS_NAME = "VFS-Emulator"
    VFS_RELEASE = "1.0"
    VFS_VERSION = "Stage-4"
    VFS_MACHINE = "x86_64"
    def __init__(self, root, vfs_path=None, script_path=None):
        self.root = root
        self.root.title("VFS Shell Emulator")
        self.root.geometry("700x450")
        self.root.configure(bg="#1e1e1e")

        self.vfs = VFS()

        self.setup_gui()
        self.print_to_output(
            "Welcome to VFS Shell. "
            "Type 'exit' to quit.\n\n"
        )
        self.print_debug_info(vfs_path, script_path)
        self.load_vfs(vfs_path)

        if script_path:
            self.execute_startup_script(script_path)

    def setup_gui(self):
        self.output = scrolledtext.ScrolledText(
            self.root, bg="#1e1e1e", fg="#00ff00",
            font=("Menlo", 13),
            insertbackground="white",
            relief=tk.FLAT, borderwidth=0
        )
        self.output.pack(
            fill=tk.BOTH, expand=True, padx=5, pady=5
        )
        self.output.config(state=tk.DISABLED)

        self.input_frame = tk.Frame(
            self.root, bg="#1e1e1e"
        )
        self.input_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.prompt = tk.Label(
            self.input_frame, text="vfs $ ",
            font=("Menlo", 13),
            bg="#1e1e1e", fg="#00aaff"
        )
        self.prompt.pack(side=tk.LEFT)

        self.entry = tk.Entry(
            self.input_frame, bg="#1e1e1e", fg="#ffffff",
            font=("Menlo", 13),
            insertbackground="white", relief=tk.FLAT
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.process_input)
        self.entry.focus()

    def print_debug_info(self, vfs_path, script_path):
        self.print_to_output(
            "--- Debug: Startup Parameters ---\n"
        )
        vfs_str = vfs_path if vfs_path else "Not specified"
        script_str = (
            script_path if script_path else "Not specified"
        )
        self.print_to_output(f"VFS Path:    {vfs_str}\n")
        self.print_to_output(
            f"Script Path: {script_str}\n"
        )
        self.print_to_output(
            "-------------------------------\n\n"
        )

    def load_vfs(self, vfs_path):
        if not vfs_path:
            self.print_to_output(
                "VFS not specified, using empty VFS.\n\n"
            )
            return
        try:
            self.vfs.load_from_zip(vfs_path)
            msg = f"VFS loaded: {vfs_path}\n\n"
            self.print_to_output(msg)
        except FileNotFoundError as err:
            self.print_to_output(f"Error: {err}\n\n")
        except ValueError as err:
            self.print_to_output(f"Error: {err}\n\n")

    def execute_startup_script(self, script_path):
        header = f"--- Executing: {script_path} ---\n"
        self.print_to_output(header)

        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                for line in f:
                    self.process_script_line(line)
            self.print_to_output(
                "--- Script finished ---\n\n"
            )
        except FileNotFoundError:
            msg = f"Error: script not found: {script_path}\n"
            self.print_to_output(msg + "\n")
        except Exception as err:
            self.print_to_output(
                f"Error reading script: {err}\n\n"
            )

    def process_script_line(self, line):
        cmd = line.strip()
        if not cmd or cmd.startswith('#'):
            return
        if cmd == "exit":
            self.print_to_output(
                "Skipping 'exit' in script.\n"
            )
            return

        self.print_to_output(f"vfs $ {cmd}\n")
        try:
            self.run_command(cmd)
        except Exception as err:
            err_msg = f"Error in '{cmd}': {err}\n"
            self.print_to_output(err_msg)

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

        self.run_command(user_input)

    def run_command(self, user_input):
        try:
            args = shlex.split(user_input)
        except ValueError as err:
            msg = f"Error: unmatched quotes ({err})\n"
            self.print_to_output(msg)
            return

        if not args:
            return

        command = args[0]
        cmd_args = args[1:]

        handlers = {
            "exit": self.handle_exit,
            "ls": lambda a: self.handle_ls(a),
            "cd": lambda a: self.handle_cd(a),
            "uname": lambda a: self.handle_uname(a),
            "rev": lambda a: self.handle_rev(a),
        }

        handler = handlers.get(command)
        if handler:
            handler(cmd_args)
        else:
            msg = f"Error: command not found: {command}\n"
            self.print_to_output(msg)


    def handle_exit(self,cmd_args):
        self.print_to_output("Exiting VFS Shell...\n")
        self.root.quit()
        self.root.destroy()

    

    def handle_cd(self, cmd_args):
        if not cmd_args:
            self.print_to_output(
                "cd: missing argument\n"
            )
            return
        try:
            self.vfs.change_dir(cmd_args[0])
        except ValueError as err:
            self.print_to_output(f"cd: {err}\n")
    def handle_ls(self, cmd_args):
        show_all = False
        long_format = False
        path = None

        for arg in cmd_args:
            if arg.startswith('-'):
                if 'a' in arg:
                    show_all = True
                if 'l' in arg:
                    long_format = True
            else:
                path = arg

        try:
            items = self.vfs.list_dir(path)
            if not show_all:
                items = [i for i in items if not i.startswith('.')]

            if long_format:
                self.print_ls_long(items, path)
            else:
                if items:
                    self.print_to_output(
                        '  '.join(items) + '\n'
                    )
                else:
                    self.print_to_output("(empty)\n")
        except ValueError as err:
            self.print_to_output(f"ls: {err}\n")

    def print_ls_long(self, items, path):
        for item in items:
            full_path = item
            if path:
                full_path = path.rstrip('/') + '/' + item
            try:
                node = self.vfs._get_node(
                    self.vfs._parse_path(full_path)
                )
                if isinstance(node, dict):
                    kind = "d"
                    size = 0
                else:
                    kind = "-"
                    size = len(node)
                info = f"{kind}  {size:>6}  {item}"
                self.print_to_output(info + '\n')
            except Exception:
                self.print_to_output(f"?  {item}\n")

    def handle_uname(self, cmd_args):
        if not cmd_args:
            self.print_to_output(self.VFS_NAME + '\n')
            return

        options = cmd_args[0]
        if not options.startswith('-'):
            self.print_to_output(
                f"uname: unknown option: {options}\n"
            )
            return

        flags = options[1:]
        if 'a' in flags:
            parts = [
                self.VFS_NAME,
                platform.node(),
                self.VFS_RELEASE,
                self.VFS_VERSION,
                self.VFS_MACHINE,
            ]
            self.print_to_output(' '.join(parts) + '\n')
            return

        result = []
        flag_map = {
            's': self.VFS_NAME,
            'n': platform.node(),
            'r': self.VFS_RELEASE,
            'v': self.VFS_VERSION,
            'm': self.VFS_MACHINE,
        }
        for flag in flags:
            if flag in flag_map:
                result.append(flag_map[flag])
            else:
                msg = f"uname: unknown option: {flag}\n"
                self.print_to_output(msg)
                return

        if result:
            self.print_to_output(' '.join(result) + '\n')

    def handle_rev(self, cmd_args):
        if not cmd_args:
            self.print_to_output("rev: missing argument\n")
            return

        target = cmd_args[0]
        try:
            content = self.vfs.read_file(target)
            lines = content.splitlines()
            for line in lines:
                self.print_to_output(line[::-1] + '\n')
        except ValueError:
            self.print_to_output(target[::-1] + '\n')


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


if __name__ == "__main__":
    args = parse_arguments()
    root = tk.Tk()
    app = VFSShell(
        root,
        vfs_path=args.vfs_path,
        script_path=args.script
    )
    root.mainloop()