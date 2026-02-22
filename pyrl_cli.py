#!/usr/bin/env python3
"""
Pyrl CLI - Command Line Interface
"""

import sys
import os
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pyrl_vm import PyrlVM
from pyrl_plugin_system import PluginManager, load_builtin_plugins
from pyrl_ai import PyrlInteractiveSession


def main():
    parser = argparse.ArgumentParser(
        description='Pyrl CLI - Execute and generate Pyrl code',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pyrl run script.pyrl           # Execute a Pyrl file
  pyrl test tests.pyrl           # Run tests
  pyrl generate "function desc"  # Generate code with AI
  pyrl repl                      # Interactive session
  pyrl plugins                   # List plugins
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Execute Pyrl file')
    run_parser.add_argument('file', help='Pyrl file to execute')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests')
    test_parser.add_argument('file', help='Test file')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate code with AI')
    gen_parser.add_argument('prompt', help='Description of code to generate')
    
    # REPL command
    subparsers.add_parser('repl', help='Interactive session')
    
    # Plugins command
    subparsers.add_parser('plugins', help='List plugins')
    
    args = parser.parse_args()
    
    # Initialize VM with plugins
    vm = PyrlVM()
    manager = PluginManager(vm)
    load_builtin_plugins(manager)
    
    if args.command == 'run':
        with open(args.file, 'r') as f:
            code = f.read()
        try:
            result = vm.execute(code)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif args.command == 'test':
        with open(args.file, 'r') as f:
            code = f.read()
        results = vm.run_tests(code)
        summary = vm.get_test_summary()
        
        print(f"\n{'='*50}")
        print(f"Tests: {summary['passed']}/{summary['total']} passed")
        print(f"Success rate: {summary['success_rate']:.1f}%")
        print('='*50)
        
        for r in results:
            status = '✓' if r.success else '✗'
            print(f"  {status} {r.name}: {r.message}")
        
        if summary['failed'] > 0:
            sys.exit(1)
    
    elif args.command == 'generate':
        ai = PyrlAI(vm)
        result = ai.generate_code(args.prompt)
        print(f"\n{'='*50}")
        print("Generated Code:")
        print('='*50)
        print(result.code)
        if result.explanation:
            print(f"\nExplanation: {result.explanation}")
        if result.plugins_needed:
            print(f"\nPlugins needed: {', '.join(result.plugins_needed)}")
    
    elif args.command == 'repl':
        session = PyrlInteractiveSession()
        print("Pyrl REPL v2.0.0")
        print("Type /help for commands, /exit to quit\n")
        
        while True:
            try:
                user_input = input("pyrl> ")
                if user_input.strip() == '/exit':
                    break
                response = session.process_input(user_input)
                print(response)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    elif args.command == 'plugins':
        print("\nLoaded Plugins:")
        print('='*50)
        for plugin in manager.list_plugins():
            print(f"\n{plugin.name} v{plugin.version}")
            print(f"  {plugin.description}")
            print(f"  State: {plugin.state.value}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
