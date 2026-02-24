# Pyrl VSCode Extension

Visual Studio Code extension for the Pyrl programming language.

## Features

### 🎨 Syntax Highlighting

Full syntax highlighting for Pyrl language constructs:

- Variables with sigils (`$scalar`, `@array`, `%hash`, `&function`)
- Keywords (`if`, `else`, `elif`, `for`, `while`, `def`, `class`)
- Built-in functions (`print`, `len`, `range`, `int`, `str`, etc.)
- Strings and comments
- Regular expressions (Perl-style)

### 📝 Code Snippets

Quick code templates for common patterns:

| Prefix | Description |
|--------|-------------|
| `pyrl-def` | Function definition |
| `pyrl-class` | Class definition |
| `pyrl-if` | If statement |
| `pyrl-if-else` | If-else statement |
| `pyrl-for` | For loop |
| `pyrl-while` | While loop |
| `pyrl-try` | Try-except block |
| `pyrl-web` | Web app handler |
| `pyrl-scalar` | Scalar variable |
| `pyrl-array` | Array variable |
| `pyrl-hash` | Hash variable |
| `pyrl-func` | Function variable |

### 🔍 Language Configuration

- **Auto-closing pairs**: `()`, `[]`, `{}`, `""`, `''`
- **Comment toggling**: `#` style comments
- **Indentation**: 4 spaces (Python-style)
- **Bracket matching**: Visual matching for `[]`, `{}`, `()`

## Installation

### From Source

```bash
cd vscode-pyrl
code --install-extension .
```

### Manual Installation

1. Copy `vscode-pyrl` folder to your VSCode extensions directory:
   - **Windows**: `%USERPROFILE%\.vscode\extensions`
   - **macOS**: `~/.vscode/extensions`
   - **Linux**: `~/.vscode/extensions`

2. Restart VSCode

### Development

```bash
# Clone repository
git clone https://github.com/pyrl-lang/pyrl.git

# Open extension folder
cd pyrl/vscode-pyrl
code .

# Press F5 to launch Extension Development Host
```

## File Association

The extension automatically activates for `.pyrl` files.

To manually set language mode:
1. Open a file
2. Press `Ctrl+Shift+P` (Cmd+Shift+P on macOS)
3. Type "Change Language Mode"
4. Select "Pyrl"

## Extension Structure

```
vscode-pyrl/
├── package.json              # Extension manifest
├── language-configuration.json # Language settings
├── syntaxes/
│   └── pyrl.tmLanguage.json  # TextMate grammar
├── snippets/
│   └── pyrl.json             # Code snippets
├── icons/
│   ├── pyrl-light.svg        # Light theme icon
│   └── pyrl-dark.svg         # Dark theme icon
└── README.md                 # This file
```

## Configuration

Add to your `settings.json`:

```json
{
    "[pyrl]": {
        "editor.tabSize": 4,
        "editor.insertSpaces": true,
        "editor.autoIndent": "advanced",
        "editor.formatOnSave": false
    }
}
```

## Known Limitations

- No semantic highlighting (planned)
- No code formatting (planned)
- No debugging support (planned)
- No IntelliSense (planned)

## Contributing

To contribute to the extension:

1. Fork the repository
2. Make your changes
3. Test in Extension Development Host
4. Submit a Pull Request

## Future Plans

- [ ] IntelliSense autocompletion
- [ ] Go to definition
- [ ] Find all references
- [ ] Code formatting
- [ ] Debugging support
- [ ] Linting integration

## License

MIT License
