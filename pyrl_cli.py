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
import re
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.vm import PyrlVM, PyrlRuntimeError
from src.core.lark_parser import print_ast as lark_print_ast, ParseErrorInfo
from src.core.lexer import tokenize
from src.core.parser import parse
from src.core.exceptions import PyrlError
from src.core.builtins import load_builtin_plugins, get_loaded_plugins


__version__ = "2.0.0"
__author__ = "Pyrl Team"


class PyrlCLI:
    """Command Line Interface for Pyrl."""

    def __init__(self, debug: bool = False, use_lark: bool = True):
        self.debug = debug
        self.use_lark = use_lark
        self.vm = PyrlVM(debug=debug)
        self.env = self.vm.env
        load_builtin_plugins(self.vm.env)
        if debug:
            print("\033[90mUsing Lark-based parser with debug mode\033[0m")

    def _format_error_type(self, error_type: str) -> str:
        """Format error type with spaces (e.g., 'PyrlRuntimeError' -> 'PYRL RUNTIME ERROR')."""
        # Insert spaces before capital letters (except the first one)
        formatted = re.sub(r'(?<!^)(?=[A-Z])', ' ', error_type)
        return formatted.upper()

    def _print_debug_error(self, error_type: str, error: Exception) -> None:
        """Print detailed debug information for ANY error."""
        if self.debug:
            import traceback
            print(f"\n\033[91m{'='*60}\033[0m", file=sys.stderr)
            print(f"\033[91m{self._format_error_type(error_type)}\033[0m", file=sys.stderr)
            print(f"\033[91m{'='*60}\033[0m", file=sys.stderr)
            print(f"\033[93mMessage:\033[0m {error}", file=sys.stderr)
            print(f"\033[93mType:\033[0m {type(error).__name__}", file=sys.stderr)
            if hasattr(error, '__traceback__') and error.__traceback__:
                print(f"\033[93mTraceback:\033[0m", file=sys.stderr)
                traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            print(f"\033[91m{'='*60}\033[0m\n", file=sys.stderr)
        else:
            print(f"\033[91m{self._format_error_type(error_type)}\033[0m {error}")

    def run_repl(self) -> None:
        """Start interactive REPL session."""
        self._print_banner()

        while True:
            try:
                lines = self._read_multiline()
                if lines is None:
                    continue

                source = "\n".join(lines)
                if not source.strip():
                    continue

                if self._handle_special_command(source.strip()):
                    continue

                result = self.vm.run(source)
                if result is not None:
                    self._print_result(result)

            except KeyboardInterrupt:
                print("\n\nInterrupted. Press Ctrl+C again to exit or type 'exit' to quit.")

            except PyrlRuntimeError as e:
                self._print_debug_error(f"\033[91mRuntime Error:\033[0m {e}", e)

            except SyntaxError as e:
                self._print_debug_error(print(str(e), file=sys.stderr), e)

            except PyrlError as e:
                self._print_debug_error(f"\033[91mPyrl Error:\033[0m {e}", e)

            except Exception as e:
                self._print_debug_error(f"\033[91mError:\033[0m {e}", e)

    def _print_banner(self) -> None:
        """Print REPL banner with PYRL logo."""

        banner = f"""
\033[96m╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   \033[92m██████╗ ██╗   ██╗ █████╗ ██╗  ██╗\033[96m                           ║
║   \033[92m██╔══██╗██║   ██║██╔══██╗██║ ██╔╝\033[96m                           ║
║   \033[92m██████╔╝██║   ██║███████║█████╔╝ \033[96m                           ║
║   \033[92m██╔══██╗██║   ██║██╔══██║██╔═██╗ \033[96m                           ║
║   \033[92m██████╔╝╚██████╔╝██║  ██║██║  ██╗\033[96m                           ║
║   \033[92m╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝\033[96m                           ║
║                                                               ║
║   \033[93mHybrid Python-Perl Language Interpreter v{__version__}\033[96m              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝\033[0m
"""
        print(banner)
        print("Type '\033[93mhelp\033[0m' for help, '\033[93mexit\033[0m' to quit")
        print("─" * 63)

    def _read_multiline(self) -> list:
        lines = []
        prompt = "\033[92mpyrl>\033[0m "
        while True:
            try:
                line = input(prompt)
                if lines and not line.strip():
                    break
                if lines and not self._needs_continuation(lines[-1]) and not line.startswith((' ', '\t')):
                    lines.append(line)
                    break
                lines.append(line)
                if not self._needs_continuation(line):
                    break
                prompt = "\033[94m....>\033[0m "
            except EOFError:
                return lines if lines else None
            except KeyboardInterrupt:
                print()
                return None
        return lines if lines else None

    def _needs_continuation(self, line: str) -> bool:
        line = line.rstrip()
        if not line:
            return False
        if line.endswith(':'):
            return True
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
        help_text = """
\033[96m╔════════════════════════════════════════════════════════════════╗
║                        \033[93mPYRL HELP\033[96m                           ║
╚════════════════════════════════════════════════════════════════╝\033[0m

\033[93mVariables (Sigils):\033[0m
    $name   - Scalar (single value)
    @array  - Array (list)
    %hash   - Hash/dictionary
    &func   - Function reference

\033[93mREPL Commands:\033[0m
    help     - Show this help
    vars     - Show all variables
    reset    - Reset VM state
    version  - Show version
    load <file> - Load and execute file
    exit     - Exit REPL

\033[93mDebugging:\033[0m
    Run with --debug flag for detailed error messages
"""
        print(help_text)

    def _print_variables(self) -> None:
        variables = self.vm.get_globals()
        if not variables:
            print("\033[90mNo variables defined.\033[0m")
            return
        print("\n\033[93mVariables:\033[0m")
        print("─" * 40)
        for name, value in sorted(variables.items()):
            if name.startswith('_') or name in ('True', 'False', 'None', 'PI', 'E', 'INF', 'NAN'):
                continue
            if isinstance(value, list):
                sigil = '@'
            elif isinstance(value, dict):
                sigil = '%'
            elif callable(value):
                sigil = '&'
            else:
                sigil = '$'
            if isinstance(value, (list, dict)):
                value_str = str(value)
                if len(value_str) > 50:
                    value_str = value_str[:47] + "..."
            elif callable(value):
                value_str = f"<function {name}>"
                sigil = ''
            else:
                value_str = repr(value)
            print(f"  {sigil}\033[92m{name}\033[0m = {value_str}")
        print()

    def _print_result(self, result) -> None:
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
        except SyntaxError as e:
            if self.debug:
                self._print_debug_error("SyntaxError", e)
            else:
                print(str(e), file=sys.stderr)
        except Exception as e:
            if self.debug:
                self._print_debug_error(type(e).__name__, e)
            else:
                print(f"\033[91mError loading file: {e}\033[0m")

    def _print_plugins(self) -> None:
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
        try:
            from src.core.builtins import _plugin_loader
            exports = _plugin_loader.load_plugin(plugin_name)
            for name, value in exports.items():
                full_name = f"{plugin_name}_{name}"
                if hasattr(self.env, 'define'):
                    self.env.define(full_name, value)
                else:
                    self.env[full_name] = value
            print(f"\033[92mPlugin '{plugin_name}' loaded successfully.\033[0m")
        except Exception as e:
            if self.debug:
                self._print_debug_error(type(e).__name__, e)
            else:
                print(f"\033[91mError loading plugin: {e}\033[0m")

    def _train_model(self) -> None:
        self._train_model_with_args("")

    def _train_model_with_args(self, args: str) -> None:
        import subprocess
        import shlex
        print("\033[96m" + "═" * 50)
        print("   Pyrl Model Training")
        print("═" * 50 + "\033[0m")
        cmd = [sys.executable, "scripts/train_model.py"]
        examples_path = None
        if args:
            try:
                parts = shlex.split(args)
            except:
                parts = args.split()
            i = 0
            while i < len(parts):
                part = parts[i]
                if part.startswith("--example=") or part.startswith("--examples="):
                    examples_path = part.split("=", 1)[1]
                elif part in ("--example", "--examples") and i + 1 < len(parts):
                    examples_path = parts[i + 1]
                    i += 1
                elif part.startswith("--"):
                    cmd.append(part)
                i += 1
        if examples_path:
            examples_file = Path(examples_path)
            if not examples_file.is_absolute():
                examples_file = Path(__file__).parent / examples_path
            if examples_file.exists():
                cmd.extend(["--examples", str(examples_file)])
        else:
            default_examples = Path(__file__).parent / "examples/10000_examples.pyrl"
            if default_examples.exists():
                cmd.extend(["--examples", str(default_examples)])
        print(f"\n\033[90mRunning: {' '.join(cmd)}\033[0m\n")
        try:
            result = subprocess.run(cmd, cwd=str(Path(__file__).parent))
            if result.returncode == 0:
                print(f"\n\033[92mTraining completed successfully!\033[0m")
            else:
                print(f"\n\033[91mTraining failed with code {result.returncode}\033[0m")
        except Exception as e:
            if self.debug:
                self._print_debug_error(type(e).__name__, e)
            else:
                print(f"\033[91mError running training: {e}\033[0m")

    def run_file(self, filepath: str) -> int:
        try:
            path = Path(filepath)
            if not path.exists():
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                return 1
            result = self.vm.run_file(str(path))
            return 0
        except SyntaxError as e:
            if self.debug:
                self._print_debug_error("SyntaxError", e)
            else:
                print(str(e), file=sys.stderr)
            return 1
        except PyrlRuntimeError as e:
            if self.debug:
                self._print_debug_error("PyrlRuntimeError", e)
            else:
                print(f"Runtime Error: {e}", file=sys.stderr)
            return 1
        except PyrlError as e:
            if self.debug:
                self._print_debug_error("PyrlError", e)
            else:
                print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            self._print_debug_error(type(e).__name__, e)
            return 1

    def run_code(self, code: str) -> int:
        try:
            result = self.vm.run(code)
            if result is not None:
                print(result)
            return 0
        except SyntaxError as e:
            if self.debug:
                self._print_debug_error("SyntaxError", e)
            else:
                print(str(e), file=sys.stderr)
            return 1
        except PyrlRuntimeError as e:
            if self.debug:
                self._print_debug_error("PyrlRuntimeError", e)
            else:
                print(f"Runtime Error: {e}", file=sys.stderr)
            return 1
        except PyrlError as e:
            if self.debug:
                self._print_debug_error("PyrlError", e)
            else:
                print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            self._print_debug_error(type(e).__name__, e)
            return 1

    def tokenize_file(self, filepath: str) -> int:
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
            if self.debug:
                self._print_debug_error(type(e).__name__, e)
            else:
                print(f"Error: {e}", file=sys.stderr)
            return 1

    def parse_file(self, filepath: str) -> int:
        try:
            path = Path(filepath)
            if not path.exists():
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                return 1
            source = path.read_text()
            if self.use_lark:
                from src.core.lark_parser import parse_lark
                ast = parse_lark(source, debug=self.debug)
                print(f"\n\033[96mAST from {filepath} (Lark parser):\033[0m")
                print("─" * 60)
                lark_print_ast(ast)
            else:
                tokens = tokenize(source)
                ast = parse(tokens)
                print(f"\n\033[96mAST from {filepath} (Legacy parser):\033[0m")
                print("─" * 60)
                self._print_ast(ast, indent=0)
            return 0
        except SyntaxError as e:
            if self.debug:
                self._print_debug_error("SyntaxError", e)
            else:
                print(str(e), file=sys.stderr)
            return 1
        except Exception as e:
            self._print_debug_error(type(e).__name__, e)
            return 1

    def _print_ast(self, node, indent: int = 0) -> None:
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
    parser.add_argument('file', nargs='?', help='Pyrl script file to execute')
    parser.add_argument('-c', '--code', metavar='CODE', help='Execute code from command line')
    parser.add_argument('-t', '--tokenize', action='store_true', help='Tokenize file and show tokens')
    parser.add_argument('-p', '--parse', action='store_true', help='Parse file and show AST')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--legacy', action='store_true', help='Use legacy parser')
    parser.add_argument('-v', '--version', action='version', version=f'Pyrl {__version__}')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    return parser


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()
    if args.no_color:
        os.environ['NO_COLOR'] = '1'
    use_lark = not args.legacy
    cli = PyrlCLI(debug=args.debug, use_lark=use_lark)
    if args.code:
        return cli.run_code(args.code)
    if args.tokenize and args.file:
        return cli.tokenize_file(args.file)
    if args.parse and args.file:
        return cli.parse_file(args.file)
    if args.file:
        return cli.run_file(args.file)
    try:
        cli.run_repl()
        return 0
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        return 0


if __name__ == '__main__':
    sys.exit(main())