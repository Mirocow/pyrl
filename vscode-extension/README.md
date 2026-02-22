# Pyrl Language Support for VSCode

This extension provides syntax highlighting, snippets, and language configuration for the **Pyrl** programming language - a hybrid Python-Perl inspired language.

## Features

- 🎨 **Syntax Highlighting** - Full syntax highlighting for all Pyrl constructs
- 📝 **Code Snippets** - Quick snippets for common patterns
- 🔧 **Language Configuration** - Bracket matching, comment toggling, and auto-closing pairs
- 🎯 **Sigil Support** - Distinct highlighting for `$scalar`, `@array`, `%hash`, and `&function` variables

## Installation

### From VSCode Marketplace
1. Open VSCode
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Pyrl Language"
4. Click Install

### Manual Installation
1. Download the `.vsix` file
2. Open VSCode
3. Go to Extensions (Ctrl+Shift+X)
4. Click the "..." menu → Install from VSIX
5. Select the downloaded file

## Supported Syntax

### Variables (Sigils)
```pyrl
$name = "John"        # Scalar ($)
@items = [1, 2, 3]    # Array (@)
%user = {"age": 25}   # Hash (%)
&greet = { ... }      # Function (&)
```

### Control Flow
```pyrl
if $x > 5 {
    # ...
} else {
    # ...
}

for $item in @array {
    # ...
}

while $condition {
    # ...
}
```

### Functions
```pyrl
&add($x, $y) = {
    return $x + $y
}

$result = &add(3, 4)
```

### Regex
```pyrl
$email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
if $email =~ $email_pattern {
    # valid email
}
```

### Tests
```pyrl
test "Math operations" {
    assert 2 + 2 == 4
    assert 10 - 5 == 5
}
```

### Vue Component Generation
```pyrl
vue "LoginForm" {
    title: "Sign In",
    username_label: "Username"
}
```

## Snippets

| Prefix | Description |
|--------|-------------|
| `var` | Scalar variable |
| `arr` | Array variable |
| `hash` | Hash variable |
| `func` | Function definition |
| `if` | If statement |
| `ifelse` | If-else statement |
| `for` | For loop |
| `while` | While loop |
| `test` | Test block |
| `assert` | Assertion |
| `vue` | Vue component |
| `regex` | Regex literal |
| `match` | Regex match |
| `print` | Print statement |
| `return` | Return statement |
| `hget` | Hash access |
| `hset` | Hash assignment |
| `aget` | Array access |
| `call` | Function call |

## File Association

Files with the `.pyrl` extension are automatically recognized.

## Color Theme Support

This extension works with any VSCode color theme. The syntax tokens are semantically categorized:

- **Keywords** - Control flow, declarations
- **Variables** - Scalars, arrays, hashes, functions
- **Strings** - Quoted strings and regex patterns
- **Numbers** - Integers, floats, hex, binary
- **Operators** - Arithmetic, comparison, logical, regex
- **Comments** - Single-line comments

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - see LICENSE file for details.
