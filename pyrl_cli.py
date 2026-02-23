#!/usr/bin/env python3
"""
Pyrl CLI - Command Line Interface for the Pyrl Language
A hybrid Python-Perl inspired language interpreter.

Usage:
    pyrl                    - Start interactive REPL
    pyrl <file.pyrl>        - Execute a Pyrl file
    pyrl -c "code"          - Execute code from string
    pyrl -t <file.pyrl>     - Tokenize file and show tokens
    pyrl -p <file.pyrl>     - Parse file and show AST
    pyrl --version          - Show version
    pyrl --help             - Show help
"""
import argparse
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.vm import PyrlVM
from src.core.lexer import tokenize
from src.core.parser import parse
from src.core.exceptions import PyrlError
from src.core.builtins import load_builtin_plugins, get_loaded_plugins


__version__ = "1.0.0"
__author__ = "Pyrl Team"


class PyrlCLI:
    """Command Line Interface for Pyrl."""
    
    def __init__(self, debug: bool = False):
        self.vm = PyrlVM(debug=debug)
        self.debug = debug
        # Load built-in plugins
        load_builtin_plugins(self.vm.env)
    
    def run_repl(self) -> None:
        """Start interactive REPL session."""
        self._print_banner()
        
        while True:
            try:
                # Read input with multi-line support
                lines = self._read_multiline()
                if lines is None:
                    continue
                
                source = "\n".join(lines)
                if not source.strip():
                    continue
                
                # Handle special commands
                if self._handle_special_command(source.strip()):
                    continue
                
                # Execute code
                result = self.vm.run(source)
                if result is not None:
                    self._print_result(result)
                    
            except KeyboardInterrupt:
                print("\n\nInterrupted. Press Ctrl+C again to exit or type 'exit' to quit.")
            except PyrlError as e:
                print(f"\033[91mError:\033[0m {e}")
            except Exception as e:
                if self.debug:
                    import traceback
                    traceback.print_exc()
                else:
                    print(f"\033[91mError:\033[0m {e}")
    
    def _print_banner(self) -> None:
        """Print REPL banner."""
        banner = """
\033[96m╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   \033[92m██████╗ ██╗   ██╗ █████╗ ██╗  ██╗\033[96m                        ║
║   \033[92m██╔══██╗██║   ██║██╔══██╗██║ ██╔╝\033[96m                        ║
║   \033[92m██████╔╝██║   ██║███████║█████╔╝ \033[96m                        ║
║   \033[92m██╔══██╗██║   ██║██╔══██║██╔═██╗ \033[96m                        ║
║   \033[92m██████╔╝╚██████╔╝██║  ██║██║  ██╗\033[96m                        ║
║   \033[92m╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝\033[96m                        ║
║                                                               ║
║   \033[93mHybrid Python-Perl Language Interpreter v{}\033[96m            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝\033[0m
""".format(__version__)
        print(banner)
        print("Type '\033[93mhelp\033[0m' for help, '\033[93mexit\033[0m' to quit")
        print("─" * 63)
    
    def _read_multiline(self) -> list:
        """Read multi-line input."""
        lines = []
        prompt = "\033[92mpyrl>\033[0m "
        
        while True:
            try:
                line = input(prompt)
                
                # Check for continuation
                if lines and not line.strip():
                    break
                if lines and not self._needs_continuation(lines[-1]) and not line.startswith((' ', '\t')):
                    lines.append(line)
                    break
                
                lines.append(line)
                
                # Check if we need more input
                if not self._needs_continuation(line):
                    break
                
                prompt = "\033[94m....>\033[0m "
                
            except EOFError:
                if lines:
                    return lines
                return None
            except KeyboardInterrupt:
                print()
                return None
        
        return lines if lines else None
    
    def _needs_continuation(self, line: str) -> bool:
        """Check if line needs continuation."""
        line = line.rstrip()
        if not line:
            return False
        
        # Check for colon (block start)
        if line.endswith(':'):
            return True
        
        # Check for unclosed brackets
        brackets = {'(': ')', '[': ']', '{': '}'}
        stack = []
        in_string = False
        string_char = None
        
        for char in line:
            if in_string:
                if char == string_char:
                    in_string = False
            elif char in '"\'':
                in_string = True
                string_char = char
            elif char in brackets:
                stack.append(brackets[char])
            elif char in brackets.values():
                if stack and stack[-1] == char:
                    stack.pop()
        
        return len(stack) > 0
    
    def _handle_special_command(self, cmd: str) -> bool:
        """Handle special REPL commands. Returns True if handled."""
        if cmd in ('exit', 'quit', 'q'):
            print("\n\033[93mGoodbye!\033[0m")
            sys.exit(0)
        
        if cmd == 'help':
            self._print_help()
            return True
        
        if cmd == 'vars':
            self._print_variables()
            return True
        
        if cmd == 'reset':
            self.vm.reset()
            print("\033[93mVM reset.\033[0m")
            return True
        
        if cmd == 'version':
            print(f"Pyrl v{__version__}")
            return True
        
        if cmd.startswith('load '):
            filepath = cmd[5:].strip()
            self._load_file(filepath)
            return True
        
        if cmd == 'plugins':
            self._print_plugins()
            return True
        
        if cmd.startswith('plugin '):
            plugin_name = cmd[7:].strip()
            self._load_plugin(plugin_name)
            return True
        
        if cmd == 'train':
            self._train_model()
            return True
        
        if cmd.startswith('train '):
            args = cmd[6:].strip()
            self._train_model_with_args(args)
            return True
        
        return False
    
    def _print_help(self) -> None:
        """Print help information."""
        help_text = """
\033[96m╔════════════════════════════════════════════════════════════════╗
║                        \033[93mPYRL HELP\033[96m                           ║
╚════════════════════════════════════════════════════════════════╝\033[0m

\033[93mVariables (Sigils):\033[0m
    $name   - Scalar (single value)
    @array  - Array (list)
    %hash   - Hash/dictionary
    &func   - Function reference

\033[93mExamples:\033[0m
    $x = 10
    $name = "Alice"
    @numbers = [1, 2, 3, 4, 5]
    %person = {name: "Bob", age: 30}

    def greet($name):
        print("Hello, " + $name + "!")
    
    greet("World")

\033[93mControl Flow:\033[0m
    if $x > 0:
        print("positive")
    elif $x < 0:
        print("negative")
    else:
        print("zero")
    
    for $i in range(10):
        print($i)
    
    while $x < 100:
        $x = $x * 2

\033[93mREPL Commands:\033[0m
    help     - Show this help
    vars     - Show all variables
    reset    - Reset VM state
    version  - Show version
    load <file> - Load and execute file
    plugins  - Show loaded plugins
    plugin <name> - Load a plugin
    train    - Train model with default examples
    train --example=<path> - Train from specific file
    train --epochs=20 --batch-size=64 - Train with options
    exit     - Exit REPL

\033[93mKeyboard Shortcuts:\033[0m
    Ctrl+C   - Cancel current input
    Ctrl+D   - Exit REPL
"""
        print(help_text)
    
    def _print_variables(self) -> None:
        """Print all variables."""
        variables = self.vm.get_globals()
        if not variables:
            print("\033[90mNo variables defined.\033[0m")
            return
        
        print("\n\033[93mVariables:\033[0m")
        print("─" * 40)
        
        for name, value in sorted(variables.items()):
            # Skip internal and builtin variables
            if name.startswith('_') or name in ('True', 'False', 'None', 'PI', 'E', 'INF', 'NAN'):
                continue
            
            # Determine sigil
            if isinstance(value, list):
                sigil = '@'
            elif isinstance(value, dict):
                sigil = '%'
            elif callable(value):
                sigil = '&'
            else:
                sigil = '$'
            
            # Format value
            if isinstance(value, (list, dict)):
                value_str = str(value)
                if len(value_str) > 50:
                    value_str = value_str[:47] + "..."
            elif callable(value):
                value_str = f"<function {name}>"
                sigil = ''  # Don't show sigil for functions in vars
            else:
                value_str = repr(value)
            
            print(f"  {sigil}\033[92m{name}\033[0m = {value_str}")
        
        print()
    
    def _print_result(self, result) -> None:
        """Print execution result."""
        if isinstance(result, bool):
            print(f"\033[93m{result}\033[0m")
        elif isinstance(result, (int, float)):
            print(f"\033[96m{result}\033[0m")
        elif isinstance(result, str):
            print(f"\033[93m'{result}'\033[0m")
        elif isinstance(result, list):
            print(f"\033[94m{result}\033[0m")
        elif isinstance(result, dict):
            print(f"\033[95m{result}\033[0m")
        else:
            print(f"\033[90m{result}\033[0m")
    
    def _load_file(self, filepath: str) -> None:
        """Load and execute a file."""
        try:
            path = Path(filepath)
            if not path.exists():
                print(f"\033[91mError: File not found: {filepath}\033[0m")
                return
            
            print(f"\033[90mLoading {filepath}...\033[0m")
            result = self.vm.run_file(str(path))
            print(f"\033[92mFile loaded successfully.\033[0m")
            if result is not None:
                self._print_result(result)
        except Exception as e:
            print(f"\033[91mError loading file: {e}\033[0m")
    
    def _print_plugins(self) -> None:
        """Print loaded plugins."""
        plugins = get_loaded_plugins()
        if not plugins:
            print("\033[90mNo plugins loaded.\033[0m")
            return
        
        print("\n\033[93mLoaded Plugins:\033[0m")
        print("─" * 40)
        
        for plugin_name, exports in sorted(plugins.items()):
            print(f"  \033[92m{plugin_name}\033[0m")
            for func_name in exports.keys():
                print(f"    └─ {func_name}")
        print()
    
    def _load_plugin(self, plugin_name: str) -> None:
        """Load a plugin by name."""
        try:
            from src.core.builtins import _plugin_loader
            exports = _plugin_loader.load_plugin(plugin_name)
            
            # Register in VM environment
            for name, value in exports.items():
                full_name = f"{plugin_name}_{name}"
                self.vm.env.define(full_name, value)
            
            print(f"\033[92mPlugin '{plugin_name}' loaded successfully.\033[0m")
            print(f"\033[90mExported functions: {', '.join(exports.keys())}\033[0m")
        except Exception as e:
            print(f"\033[91mError loading plugin: {e}\033[0m")
    
    def _train_model(self) -> None:
        """Train model with default settings."""
        self._train_model_with_args("")
    
    def _train_model_with_args(self, args: str) -> None:
        """Train model with specified arguments."""
        import subprocess
        import shlex
        
        print("\033[96m" + "═" * 50)
        print("   Pyrl Model Training")
        print("═" * 50 + "\033[0m")
        
        # Build command
        cmd = [sys.executable, "scripts/train_model.py"]
        
        # Parse arguments with proper handling
        examples_path = None
        epochs = None
        batch_size = None
        learning_rate = None
        hidden_size = None
        layers = None
        output_path = None
        
        if args:
            # Split args properly (handles quoted strings)
            try:
                parts = shlex.split(args)
            except:
                parts = args.split()
            
            i = 0
            while i < len(parts):
                part = parts[i]
                
                # Handle --example= or --examples=
                if part.startswith("--example="):
                    examples_path = part.split("=", 1)[1]
                elif part.startswith("--examples="):
                    examples_path = part.split("=", 1)[1]
                elif part in ("--example", "--examples"):
                    if i + 1 < len(parts):
                        examples_path = parts[i + 1]
                        i += 1
                
                # Handle --epochs=
                elif part.startswith("--epochs="):
                    epochs = part.split("=", 1)[1]
                elif part == "--epochs":
                    if i + 1 < len(parts):
                        epochs = parts[i + 1]
                        i += 1
                
                # Handle --batch-size=
                elif part.startswith("--batch-size="):
                    batch_size = part.split("=", 1)[1]
                elif part == "--batch-size":
                    if i + 1 < len(parts):
                        batch_size = parts[i + 1]
                        i += 1
                
                # Handle --learning-rate=
                elif part.startswith("--learning-rate="):
                    learning_rate = part.split("=", 1)[1]
                elif part == "--learning-rate":
                    if i + 1 < len(parts):
                        learning_rate = parts[i + 1]
                        i += 1
                
                # Handle --hidden-size=
                elif part.startswith("--hidden-size="):
                    hidden_size = part.split("=", 1)[1]
                elif part == "--hidden-size":
                    if i + 1 < len(parts):
                        hidden_size = parts[i + 1]
                        i += 1
                
                # Handle --layers=
                elif part.startswith("--layers="):
                    layers = part.split("=", 1)[1]
                elif part == "--layers":
                    if i + 1 < len(parts):
                        layers = parts[i + 1]
                        i += 1
                
                # Handle --output=
                elif part.startswith("--output="):
                    output_path = part.split("=", 1)[1]
                elif part == "--output":
                    if i + 1 < len(parts):
                        output_path = parts[i + 1]
                        i += 1
                
                # Pass through other args
                elif part.startswith("--"):
                    cmd.append(part)
                
                i += 1
        
        # Add examples path
        if examples_path:
            # Resolve path
            examples_file = Path(examples_path)
            if not examples_file.is_absolute():
                examples_file = Path(__file__).parent / examples_path
            if examples_file.exists():
                cmd.extend(["--examples", str(examples_file)])
                print(f"\033[93mExamples file: {examples_file}\033[0m")
            else:
                print(f"\033[91mWarning: Examples file not found: {examples_path}\033[0m")
                # Try default
                default_examples = Path(__file__).parent / "examples/10000_examples.pyrl"
                if default_examples.exists():
                    cmd.extend(["--examples", str(default_examples)])
                    print(f"\033[93mUsing default: {default_examples}\033[0m")
        else:
            # Use default examples
            default_examples = Path(__file__).parent / "examples/10000_examples.pyrl"
            if default_examples.exists():
                cmd.extend(["--examples", str(default_examples)])
                print(f"\033[93mExamples file: {default_examples}\033[0m")
        
        # Add other parameters
        if epochs:
            cmd.extend(["--epochs", epochs])
            print(f"\033[93mEpochs: {epochs}\033[0m")
        if batch_size:
            cmd.extend(["--batch-size", batch_size])
            print(f"\033[93mBatch size: {batch_size}\033[0m")
        if learning_rate:
            cmd.extend(["--learning-rate", learning_rate])
            print(f"\033[93mLearning rate: {learning_rate}\033[0m")
        if hidden_size:
            cmd.extend(["--hidden-size", hidden_size])
            print(f"\033[93mHidden size: {hidden_size}\033[0m")
        if layers:
            cmd.extend(["--layers", layers])
            print(f"\033[93mLayers: {layers}\033[0m")
        if output_path:
            cmd.extend(["--output", output_path])
            print(f"\033[93mOutput: {output_path}\033[0m")
        
        print(f"\n\033[90mRunning: {' '.join(cmd)}\033[0m\n")
        
        try:
            result = subprocess.run(cmd, cwd=str(Path(__file__).parent))
            if result.returncode == 0:
                print(f"\n\033[92mTraining completed successfully!\033[0m")
                print(f"\033[90mModel saved to: models/pyrl-model/\033[0m")
            else:
                print(f"\n\033[91mTraining failed with code {result.returncode}\033[0m")
        except Exception as e:
            print(f"\033[91mError running training: {e}\033[0m")
    
    def run_file(self, filepath: str) -> int:
        """Execute a Pyrl file. Returns exit code."""
        try:
            path = Path(filepath)
            if not path.exists():
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                return 1
            
            result = self.vm.run_file(str(path))
            return 0
        except PyrlError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            if self.debug:
                import traceback
                traceback.print_exc()
            return 1
    
    def run_code(self, code: str) -> int:
        """Execute code from string. Returns exit code."""
        try:
            result = self.vm.run(code)
            if result is not None:
                print(result)
            return 0
        except PyrlError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            if self.debug:
                import traceback
                traceback.print_exc()
            return 1
    
    def tokenize_file(self, filepath: str) -> int:
        """Tokenize a file and show tokens. Returns exit code."""
        try:
            path = Path(filepath)
            if not path.exists():
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                return 1
            
            source = path.read_text()
            tokens = tokenize(source)
            
            print(f"\n\033[96mTokens from {filepath}:\033[0m")
            print("─" * 60)
            
            for token in tokens:
                if token.type.name == 'EOF':
                    continue
                value_str = f" \033[93m{repr(token.value)}\033[0m" if token.value is not None else ""
                print(f"  \033[92m{token.type.name:15}\033[0m {value_str}")
            
            print(f"\n\033[90mTotal tokens: {len(tokens)}\033[0m")
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def parse_file(self, filepath: str) -> int:
        """Parse a file and show AST. Returns exit code."""
        try:
            path = Path(filepath)
            if not path.exists():
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                return 1
            
            source = path.read_text()
            tokens = tokenize(source)
            ast = parse(tokens)
            
            print(f"\n\033[96mAST from {filepath}:\033[0m")
            print("─" * 60)
            self._print_ast(ast, indent=0)
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def _print_ast(self, node, indent: int = 0) -> None:
        """Print AST node tree."""
        prefix = "  " * indent
        node_type = type(node).__name__
        
        if hasattr(node, '__dataclass_fields__'):
            print(f"{prefix}\033[92m{node_type}\033[0m")
            for field_name in node.__dataclass_fields__:
                value = getattr(node, field_name)
                if field_name in ('line', 'column'):
                    continue
                if isinstance(value, list):
                    if value:
                        print(f"{prefix}  \033[94m{field_name}:\033[0m")
                        for item in value:
                            self._print_ast(item, indent + 2)
                elif hasattr(value, '__dataclass_fields__'):
                    print(f"{prefix}  \033[94m{field_name}:\033[0m")
                    self._print_ast(value, indent + 2)
                else:
                    print(f"{prefix}  \033[94m{field_name}:\033[0m {value}")
        else:
            print(f"{prefix}{node}")


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog='pyrl',
        description='Pyrl Language Interpreter - A hybrid Python-Perl language',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    pyrl                      Start interactive REPL
    pyrl script.pyrl          Execute a script file
    pyrl -c '$x = 10'         Execute code from command line
    pyrl -t script.pyrl       Show tokens
    pyrl -p script.pyrl       Show AST

For more information, visit: https://github.com/pyrl-lang/pyrl
"""
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='Pyrl script file to execute'
    )
    
    parser.add_argument(
        '-c', '--code',
        metavar='CODE',
        help='Execute code from command line'
    )
    
    parser.add_argument(
        '-t', '--tokenize',
        action='store_true',
        help='Tokenize file and show tokens'
    )
    
    parser.add_argument(
        '-p', '--parse',
        action='store_true',
        help='Parse file and show AST'
    )
    
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'Pyrl {__version__}'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    return parser


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Disable colors if requested
    if args.no_color:
        os.environ['NO_COLOR'] = '1'
    
    # Create CLI instance
    cli = PyrlCLI(debug=args.debug)
    
    # Handle different modes
    if args.code:
        return cli.run_code(args.code)
    
    if args.tokenize and args.file:
        return cli.tokenize_file(args.file)
    
    if args.parse and args.file:
        return cli.parse_file(args.file)
    
    if args.file:
        return cli.run_file(args.file)
    
    # No file specified, start REPL
    try:
        cli.run_repl()
        return 0
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
