# Pyrl Documentation

## Table of Contents

1. [Getting Started](#getting-started)
2. [Language Reference](#language-reference)
3. [Built-in Functions](#built-in-functions)
4. [Plugin System](#plugin-system)
5. [AI Assistant](#ai-assistant)
6. [Testing](#testing)
7. [Vue Generation](#vue-generation)
8. [Docker Deployment](#docker-deployment)

---

## Getting Started

### Installation

```bash
# Clone repository
git clone https://github.com/pyrl-ecosystem/pyrl.git
cd pyrl

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install
pip install -e ".[dev]"
```

### Hello World

```python
from pyrl_vm import PyrlVM

vm = PyrlVM()
vm.execute('print("Hello, World!")')
```

---

## Language Reference

### Variables

Pyrl uses sigils to denote variable types:

| Sigil | Type | Example |
|-------|------|---------|
| `$` | Scalar | `$name = "Alice"` |
| `@` | Array | `@items = [1, 2, 3]` |
| `%` | Hash | `%user = {"name": "Bob"}` |
| `&` | Function | `&greet() = { ... }` |

### Data Types

```pyrl
# Strings
$name = "Alice"
$single = 'Single quotes'

# Numbers
$int = 42
$float = 3.14
$negative = -10

# Booleans
$true_val = true
$false_val = false

# None
$empty = none
$null = null
```

### Arrays

```pyrl
@fruits = ["apple", "banana", "cherry"]

# Access
$first = @fruits[0]

# Modify
@fruits[0] = "avocado"

# Add
&push(@fruits, "date")

# Remove
$last = &pop(@fruits)

# Length
$count = &len(@fruits)
```

### Hashes

```pyrl
%user = {
    "name": "Alice",
    "age": 30,
    "active": true
}

# Access
$name = %user["name"]

# Modify
%user["email"] = "alice@example.com"

# Keys and values
@keys = &keys(%user)
@values = &values(%user)
```

### Functions

```pyrl
# Simple function
&greet($name) = {
    return "Hello, " + $name + "!"
}

# Multiple parameters
&add($a, $b) = {
    return $a + $b
}

# Recursive
&factorial($n) = {
    if $n <= 1 {
        return 1
    }
    return $n * &factorial($n - 1)
}

# Call
$message = &greet("World")
$sum = &add(5, 3)
```

### Control Flow

```pyrl
# If statement
if $score >= 90 {
    $grade = "A"
}

# If-else
if $x > 0 {
    print("positive")
} else {
    print("non-positive")
}

# For loop
for $item in @items {
    print($item)
}

# While loop
while $count < 10 {
    $count = $count + 1
}
```

### Regex

```pyrl
$email = "user@example.com"
$pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Match
if $email =~ $pattern {
    print("Valid email")
}

# Not match
if $email !~ $pattern {
    print("Invalid email")
}
```

---

## Built-in Functions

### String Functions

| Function | Description | Example |
|----------|-------------|---------|
| `&upper($s)` | Uppercase | `&upper("hello")` → `"HELLO"` |
| `&lower($s)` | Lowercase | `&lower("HELLO")` → `"hello"` |
| `&trim($s)` | Remove whitespace | `&trim("  hi  ")` → `"hi"` |
| `&split($s, $d)` | Split string | `&split("a,b", ",")` → `["a", "b"]` |
| `&join(@arr, $d)` | Join array | `&join(["a", "b"], "-")` → `"a-b"` |
| `&str($x)` | Convert to string | `&str(42)` → `"42"` |

### Array Functions

| Function | Description | Example |
|----------|-------------|---------|
| `&len($x)` | Length | `&len(@arr)` |
| `&push(@arr, $x)` | Add to end | `&push(@arr, 5)` |
| `&pop(@arr)` | Remove from end | `&pop(@arr)` |
| `&min(@arr)` | Minimum | `&min([3, 1, 2])` → `1` |
| `&max(@arr)` | Maximum | `&max([3, 1, 2])` → `3` |
| `&sum(@arr)` | Sum | `&sum([1, 2, 3])` → `6` |
| `&sorted(@arr)` | Sort | `&sorted([3, 1, 2])` → `[1, 2, 3]` |
| `&reversed(@arr)` | Reverse | `&reversed([1, 2, 3])` → `[3, 2, 1]` |
| `&range($n)` | Range | `&range(5)` → `[0, 1, 2, 3, 4]` |

### Hash Functions

| Function | Description | Example |
|----------|-------------|---------|
| `&keys(%h)` | Get keys | `&keys(%user)` |
| `&values(%h)` | Get values | `&values(%user)` |

### Type Functions

| Function | Description | Example |
|----------|-------------|---------|
| `&type($x)` | Get type name | `&type(42)` → `"int"` |
| `&int($x)` | Convert to int | `&int("42")` → `42` |
| `&float($x)` | Convert to float | `&float("3.14")` → `3.14` |

---

## Plugin System

### Using Plugins

```python
from pyrl_vm import PyrlVM
from pyrl_plugin_system import PluginManager, load_builtin_plugins

vm = PyrlVM()
manager = PluginManager(vm)
load_builtin_plugins(manager)

# Now use plugin functions
vm.execute('$root = &sqrt(16)')      # 4.0
vm.execute('$now = &now()')          # Current datetime
vm.execute('$hash = &sha256("hi")')  # SHA-256 hash
```

### Creating Plugins

```python
# my_plugin/plugin.py
from pyrl_plugin_system import PluginBase

class MyPlugin(PluginBase):
    NAME = "my_plugin"
    VERSION = "1.0.0"
    DESCRIPTION = "My custom plugin"
    AUTHOR = "Developer"
    
    def on_load(self):
        self.register_function("double", self._double)
    
    def _double(self, x):
        return x * 2

plugin_class = MyPlugin
```

```json
// my_plugin/plugin.json
{
    "name": "my_plugin",
    "version": "1.0.0",
    "description": "My custom plugin",
    "author": "Developer",
    "main": "plugin.py",
    "functions": ["double"]
}
```

---

## AI Assistant

### Code Generation

```python
from pyrl_ai import PyrlAI

ai = PyrlAI()

# Generate code
result = ai.generate_code("Create a function to calculate factorial")
print(result.code)

# Explain code
explanation = ai.explain_code(result.code)
print(explanation)
```

### Interactive Session

```python
from pyrl_ai import PyrlInteractiveSession

session = PyrlInteractiveSession()

# Generate
response = session.process_input(
    "Create a test for user authentication"
)

# Execute
response = session.process_input("/run $x = 5 + 3")
```

---

## Testing

### Test Blocks

```pyrl
test "Math Operations" {
    assert 1 + 1 == 2
    assert 2 * 3 == 6
    assert 10 / 2 == 5
}

test "String Operations" {
    assert &upper("hello") == "HELLO"
    assert &len("test") == 4
}
```

### Running Tests

```python
from pyrl_vm import PyrlVM

vm = PyrlVM()
results = vm.run_tests('''
    test "Example" {
        assert 1 == 1
    }
''')

summary = vm.get_test_summary()
print(f"Passed: {summary['passed']}/{summary['total']}")
```

---

## Vue Generation

### Basic Component

```pyrl
vue "UserCard" {
    name: "Alice",
    email: "alice@example.com"
}
```

### With Variables

```pyrl
$title = "Welcome"
@items = ["Item 1", "Item 2"]

vue "Dashboard" {
    title: $title,
    items: @items
}
```

---

## Docker Deployment

### Build Images

```bash
# Production
docker build -f docker/Dockerfile --target production -t pyrl:latest .

# Development
docker build -f docker/Dockerfile --target development -t pyrl:dev .

# Training (GPU)
docker build -f docker/Dockerfile --target training -t pyrl:training .

# API Server
docker build -f docker/Dockerfile --target api -t pyrl:api .
```

### Run Containers

```bash
# Production
docker run -it pyrl:latest

# Development
docker run -v ./src:/app/src -it pyrl:dev

# API Server
docker run -p 8000:8000 pyrl:api
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/execute` | POST | Execute Pyrl code |
| `/test` | POST | Run tests |
| `/generate` | POST | AI code generation |
| `/plugins` | GET | List plugins |

---

## Version

Pyrl v2.0.0 - Released 2024-02-22
