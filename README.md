# VFS Shell Emulator

A command-line shell emulator for a UNIX-like OS with a graphical interface.

## Stage 1: REPL (Read-Eval-Print Loop)

### Implemented functionality:
- A graphical user interface (GUI) based on `tkinter`, styled to resemble a terminal.
- Window title: `VFS`.
- A command-line parser with correct handling of quoted arguments (based on `shlex`).
- Dummy commands: `ls`, `cd` (display the command name and a list of arguments).
- The `exit` command to terminate the emulator.
- Handling of syntax errors and unknown commands.
### Examples:
VFS Shell Emulator. Type 'exit' to quit.

vfs> ls
[ls] Executed with arguments: []

vfs> ls -l /home/user
[ls] Executed with arguments: ['-l', '/home/user']

vfs> cd "My Documents"
[cd] Executed with arguments: ['My Documents']

vfs> cd 'folder with "quotes"'
[cd] Executed with arguments: ['folder with "quotes"']

vfs> unknown_cmd
vfs: unknown_cmd: command not found

vfs> cd "unclosed quote
vfs: parse error: No closing quotation

vfs> exit

### Stage 2: Configuration

Extended functionality:
- Command-line arguments parsing (`--vfs-path`, `--script`)
- Debug output of all provided parameters at startup
- Startup script execution with sequential command processing
- Error handling during script execution (skips erroneous lines)
- Imitation of user dialogue (displays both input and output)