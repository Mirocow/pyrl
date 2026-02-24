# Pyrl Language Support for VS Code

This extension provides syntax highlighting, snippets, and language support for the [Pyrl](http://178.140.10.58:8082/ai/pyrl-project.git) programming language.

## Features

- **Syntax Highlighting**: Full support for Pyrl syntax including:
  - Sigil-based variables (`$scalar`, `@array`, `%hash`, `&function`)
  - Keywords (`if`, `elif`, `else`, `for`, `while`, `def`, `class`, etc.)
  - Built-in functions
  - Strings with interpolation
  - Regular expressions
  - Comments

- **Code Snippets**: Quick snippets for common patterns:
  - Function definitions (`def`)
  - Anonymous functions (`afunc`)
  - Class definitions (`class`)
  - Control flow (`if`, `ifelse`, `for`, `while`)
  - HTTP handlers (`handler`)
  - Variables (`scalar`, `array`, `hash`)

- **Language Configuration**:
  - Auto-closing brackets and quotes
  - Comment toggling
  - Bracket matching
  - Indentation rules

## Installation

### From VSIX

1. Download the `.vsix` file
2. Open VS Code
3. Go to Extensions (Ctrl+Shift+X)
4. Click the three dots menu → Install from VSIX
5. Select the downloaded file

### Manual Installation

1. Clone or download this repository
2. Copy the `vscode-pyrl` folder to your VS Code extensions directory:
   - Windows: `%USERPROFILE%\.vscode\extensions`
   - macOS/Linux: `~/.vscode/extensions`
3. Restart VS Code

## Usage

Open any `.pyrl` file and enjoy syntax highlighting!

### Example

```pyrl
# Variables with sigils
$name = "Alice"
@items = [1, 2, 3]
%person = {name: "Bob", age: 30}

# Function definition
def greet($name):
    print("Hello, " + $name + "!")

# Anonymous function
&double($x) = {
    return $x * 2
}

# Class definition
class Person {
    prop name = "Unknown"
    prop age = 0
    
    init($name, $age) = {
        $name = $name;
        $age = $age
    }
    
    method greet() = {
        return "Hi, I'm " + $name
    }
}

# HTTP handler for web server
def handle_request($method, $path, %headers, $body):
    if $path == "/" and $method == "GET":
        return html_response("<h1>Hello!</h1>")
    return html_response("Not Found", 404)

$app = {handle: &handle_request}
```

## Snippets

| Prefix | Description |
|--------|-------------|
| `def` | Function definition |
| `afunc` | Anonymous function with block syntax |
| `class` | Class with properties and methods |
| `if` | If statement |
| `ifelse` | If-else statement |
| `for` | For loop |
| `while` | While loop |
| `test` | Test block |
| `handler` | HTTP request handler |
| `scalar` | Scalar variable |
| `array` | Array variable |
| `hash` | Hash variable |

## License

MIT License

## Links

- [Pyrl Repository](http://178.140.10.58:8082/ai/pyrl-project.git)
- [Pyrl Documentation](https://github.com/pyrl-lang/pyrl)
