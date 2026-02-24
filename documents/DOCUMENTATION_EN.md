# Pyrl Language Documentation

**Version:** 2.3.0  
**Last Updated:** 2025-02-24

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Syntax](#syntax)
5. [Variables and Sigils](#variables-and-sigils)
6. [Data Types](#data-types)
7. [Operators](#operators)
8. [Control Flow](#control-flow)
9. [Functions](#functions)
10. [Classes and Objects](#classes-and-objects)
11. [Built-in Functions](#built-in-functions)
12. [SQLite Database](#sqlite-database) *(NEW v2.3)*
13. [Plugin System](#plugin-system)
14. [Model Training](#model-training)
15. [API Server](#api-server)
16. [Docker](#docker)
17. [Language Grammar](#language-grammar) *(NEW v2.2)*
18. [Examples](#examples)

---

## Introduction

Pyrl is a hybrid programming language inspired by Python and Perl. It combines the clean syntax of Python with Perl's powerful sigil system, providing a unique programming experience.

### Key Features

- **Variable Sigils**: `$scalar`, `@array`, `%hash`, `&function`
- **Python Syntax**: Indentation-based blocks instead of braces
- **Dynamic Typing**: Runtime type checking
- **Rich Standard Library**: Math, strings, lists, hashes
- **Plugin System**: Extensible architecture
- **HTTP/JSON**: Built-in web request support
- **Model Training**: Train models on Pyrl code examples

---

## Installation

### From Source

```bash
# Clone repository
git clone http://178.140.10.58:8082/ai/pyrl-project.git
cd pyrl-project

# Install dependencies
pip install -r requirements.txt

# Development install
pip install -e .
```

### Using Docker

```bash
# Build image
docker build -f docker/Dockerfile.server -t pyrl-server:latest .

# Run container
docker run -p 8000:8000 pyrl-server:latest
```

### Verify Installation

```bash
# Start REPL
python pyrl_cli.py

# Check version
python pyrl_cli.py --version
```

---

## Quick Start

### Hello World

```pyrl
print("Hello, World!")
```

### Variables

```pyrl
$name = "Alice"
$age = 30
@scores = [95, 87, 92, 88]
%person = {name: "Bob", age: 25}
```

### Functions

```pyrl
def greet($name):
    print("Hello, " + $name + "!")

greet("World")
```

### Loops

```pyrl
for $i in range(5):
    print($i)
```

---

## Syntax

### Program Structure

Pyrl programs consist of a sequence of statements. Code blocks are defined by indentation (like Python), not braces.

```pyrl
# Comment
$x = 10

if $x > 0:
    # Indented block
    print("Positive")
elif $x < 0:
    print("Negative")
else:
    print("Zero")
```

### Indentation

Use 4 spaces for indentation (recommended) or tabs. Mixing is not allowed.

```pyrl
# Correct
if True:
    print("OK")
    if False:
        print("Nested")

# Incorrect (mixed indentation)
if True:
        print("Tab")
    print("Spaces")  # Error!
```

---

## Variables and Sigils

### Sigils

Pyrl uses sigils to denote variable types:

| Sigil | Type | Description |
|-------|------|-------------|
| `$` | Scalar | Single value (number, string, boolean) |
| `@` | Array | Ordered list of values |
| `%` | Hash | Key-value dictionary |
| `&` | Function | Function reference |

### Scalars

```pyrl
$name = "Alice"
$age = 30
$pi = 3.14159
$active = True
```

### Arrays

```pyrl
@numbers = [1, 2, 3, 4, 5]
@mixed = [1, "two", 3.0, True]
@empty = []

# Index access
$first = @numbers[0]
$last = @numbers[-1]

# Slicing
@subset = @numbers[1:3]
```

### Hashes

```pyrl
%person = {name: "Alice", age: 30, active: True}

# Key access
$name = %person{name}
$age = %person{"age"}

# Add/modify
%person{email} = "alice@example.com"
```

### Function References

```pyrl
def double($x):
    return $x * 2

&func = &double
$result = &func(5)  # 10
```

---

## Data Types

### Numbers

```pyrl
$int = 42
$float = 3.14159
$neg = -17
$hex = 0xFF
$bin = 0b1010
$sci = 1.5e10
```

### Strings

```pyrl
$single = 'Hello'
$double = "World"
$multi = """
Multi-line
string
"""

# Interpolation (in double quotes)
$name = "Alice"
$greeting = "Hello, $name!"
```

### Booleans

```pyrl
$true = True
$false = False
```

### None

```pyrl
$value = None
```

---

## Operators

### Arithmetic

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `5 + 3` → `8` |
| `-` | Subtraction | `5 - 3` → `2` |
| `*` | Multiplication | `5 * 3` → `15` |
| `/` | Division | `6 / 3` → `2.0` |
| `//` | Floor division | `7 // 3` → `2` |
| `%` | Modulo | `7 % 3` → `1` |
| `**` | Exponentiation | `2 ** 3` → `8` |

### Comparison

| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Equal | `5 == 5` → `True` |
| `!=` | Not equal | `5 != 3` → `True` |
| `<` | Less than | `3 < 5` → `True` |
| `>` | Greater than | `5 > 3` → `True` |
| `<=` | Less or equal | `3 <= 3` → `True` |
| `>=` | Greater or equal | `5 >= 3` → `True` |

### Logical

| Operator | Description | Example |
|----------|-------------|---------|
| `and` | Logical AND | `True and False` → `False` |
| `or` | Logical OR | `True or False` → `True` |
| `not` | Logical NOT | `not True` → `False` |

---

## Control Flow

### Conditionals (if/elif/else)

```pyrl
$x = 10

if $x > 0:
    print("Positive")
elif $x < 0:
    print("Negative")
else:
    print("Zero")
```

### For Loop

```pyrl
# Range iteration
for $i in range(5):
    print($i)

# Array iteration
@items = ["apple", "banana", "orange"]
for $item in @items:
    print($item)

# Iteration with index
for $i, $item in enumerate(@items):
    print($i + ": " + $item)
```

### While Loop

```pyrl
$x = 0
while $x < 10:
    print($x)
    $x = $x + 1
```

### break and continue

```pyrl
for $i in range(10):
    if $i == 3:
        continue  # Skip 3
    if $i == 7:
        break     # Stop at 7
    print($i)
```

---

## Functions

### Function Definition

```pyrl
def greet($name):
    print("Hello, " + $name + "!")

greet("Alice")
```

### Return Value

```pyrl
def add($a, $b):
    return $a + $b

$result = add(5, 3)  # 8
```

### Default Arguments

```pyrl
def greet($name, $greeting = "Hello"):
    print($greeting + ", " + $name + "!")

greet("Alice")        # Hello, Alice!
greet("Bob", "Hi")    # Hi, Bob!
```

### *args and **kwargs

```pyrl
def sum_all(*$numbers):
    $total = 0
    for $n in $numbers:
        $total = $total + $n
    return $total

$result = sum_all(1, 2, 3, 4, 5)  # 15
```

### Lambda Functions

```pyrl
$square = lambda $x: $x * $x
$result = $square(5)  # 25

# With map
@doubled = map(lambda $x: $x * 2, [1, 2, 3])
```

---

## Classes and Objects

### Class Definition

```pyrl
class Person:
    def __init__($self, $name, $age):
        $self.name = $name
        $self.age = $age
    
    def greet($self):
        print("Hello, I'm " + $self.name)
    
    def get_age($self):
        return $self.age

# Create instance
$alice = Person("Alice", 30)
$alice.greet()
$age = $alice.get_age()
```

### Inheritance

```pyrl
class Student(Person):
    def __init__($self, $name, $age, $grade):
        $self.name = $name
        $self.age = $age
        $self.grade = $grade
    
    def study($self):
        print($self.name + " is studying in grade " + $self.grade)
```

---

## Built-in Functions

### I/O

| Function | Description |
|----------|-------------|
| `print(*args)` | Print to console |
| `input(prompt)` | Read from console |

### Types

| Function | Description |
|----------|-------------|
| `int(x)` | Convert to integer |
| `float(x)` | Convert to float |
| `str(x)` | Convert to string |
| `bool(x)` | Convert to boolean |
| `list(x)` | Convert to list |
| `dict(x)` | Convert to dictionary |
| `type(x)` | Get type |

### Math

| Function | Description |
|----------|-------------|
| `abs(x)` | Absolute value |
| `round(x, n)` | Round number |
| `min(*args)` | Minimum value |
| `max(*args)` | Maximum value |
| `sum(iter)` | Sum of values |
| `pow(x, y)` | Power |
| `sqrt(x)` | Square root |
| `sin(x)`, `cos(x)`, `tan(x)` | Trigonometry |
| `log(x, base)` | Logarithm |
| `exp(x)` | Exponential |
| `floor(x)`, `ceil(x)` | Floor/Ceiling |

### Strings

| Function | Description |
|----------|-------------|
| `lower(s)` | Lowercase |
| `upper(s)` | Uppercase |
| `strip(s)` | Strip whitespace |
| `split(s, sep)` | Split string |
| `join(sep, list)` | Join strings |
| `replace(s, old, new)` | Replace |
| `find(s, sub)` | Find substring |
| `startswith(s, prefix)` | Starts with |
| `endswith(s, suffix)` | Ends with |

### Lists

| Function | Description |
|----------|-------------|
| `append(list, x)` | Append element |
| `extend(list, items)` | Extend list |
| `insert(list, i, x)` | Insert element |
| `remove(list, x)` | Remove element |
| `pop(list, i)` | Pop element |
| `sort(list)` | Sort list |
| `reverse(list)` | Reverse list |
| `len(list)` | Length |

### Hashes

| Function | Description |
|----------|-------------|
| `keys(dict)` | Get keys |
| `values(dict)` | Get values |
| `items(dict)` | Key-value pairs |
| `get(dict, key, default)` | Get value |

### Regular Expressions

| Function | Description |
|----------|-------------|
| `re_match(pattern, string)` | Match at start |
| `re_search(pattern, string)` | Search in string |
| `re_findall(pattern, string)` | Find all matches |
| `re_sub(pattern, repl, string)` | Replace by pattern |

### HTTP and JSON

| Function | Description |
|----------|-------------|
| `http_get(url, timeout)` | HTTP GET request |
| `http_post(url, data, timeout)` | HTTP POST request |
| `json_parse(string)` | Parse JSON |
| `json_stringify(obj, indent)` | Serialize to JSON |

### Environment *(NEW v2.3)*

| Function | Description |
|----------|-------------|
| `env_get(key, default)` | Get environment variable |
| `env_set(key, value)` | Set environment variable |
| `env_keys()` | List all environment variables |

### Database *(NEW v2.3)*

| Function | Description |
|----------|-------------|
| `db_connect(filename)` | Connect to SQLite database |
| `db_close(handle)` | Close connection |
| `db_execute(handle, sql, params)` | Execute SQL (INSERT, UPDATE, DELETE) |
| `db_query(handle, sql, params)` | SELECT query (all rows) |
| `db_query_one(handle, sql, params)` | SELECT query (one row) |
| `db_begin(handle)` | Begin transaction |
| `db_commit(handle)` | Commit transaction |
| `db_rollback(handle)` | Rollback transaction |
| `db_tables(handle)` | List tables |

---

## SQLite Database *(NEW v2.3)*

Pyrl has built-in SQLite support for persistent data storage.

### Automatic Database Creation

When running a web application, the database is automatically created in the `data/` folder:

```bash
# Database created with pyrl file name
python scripts/run_web_app.py --file examples/web_server_auth.pyrl
# Database: data/web_server_auth.db
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `PYRL_DB_PATH` | Full path to database file |
| `PYRL_APP_NAME` | Application name (pyrl filename) |
| `PYRL_DATA_DIR` | Data directory (`data/`) |
| `PYRL_PORT` | Server port |
| `PYRL_HOST` | Server host |

### Usage in Code

```pyrl
# Get database path from environment
$DB_PATH = env_get("PYRL_DB_PATH", "data/app.db")

# Connect to database
$db = db_connect($DB_PATH)

# Create table
db_execute($db, """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'User'
    )
""")

# Insert data
db_execute($db, "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    ["admin", "secret123", "Administrator"])

# Query data
$result = db_query($db, "SELECT * FROM users WHERE role = ?", ["Administrator"])
for $user in $result["rows"]:
    print($user["username"])
```

---

## Plugin System

### Loading Built-in Plugins

```pyrl
# load_builtin_plugins() loads all built-in functions
# and returns them as a dictionary
$plugins = load_builtin_plugins()
$plugins{"print"}("Hello!")
```

### Registering Custom Plugin

```python
# In Python code
from src.core.builtins import register_plugin

def my_function(x):
    return x * 2

register_plugin("myplugin", {"double": my_function})
```

### Using in Pyrl

```pyrl
$result = myplugin_double(5)  # 10
```

### PYRL_PLUGINS_PATH Environment Variable

```bash
export PYRL_PLUGINS_PATH=/path/to/plugins:/another/path
python pyrl_cli.py
```

---

## Model Training

Pyrl includes a language model training system that learns from code examples. The model learns Pyrl syntax and patterns.

### Model Structure

```
models/pyrl-model/
├── config.json           # Model configuration (768 hidden, 12 layers)
├── pytorch_model.bin     # Model weights
├── vocab.json           # Token vocabulary (1778 tokens)
├── tokenizer_config.json # Tokenizer configuration
├── special_tokens_map.json
└── training_stats.json  # Training statistics
```

### Training via CLI

In the interactive REPL:

```
pyrl> train                          # Train with default settings
pyrl> train --epochs 20 --batch-size 64
pyrl> train --examples path/to/examples.pyrl
```

### Training via Makefile

```bash
make train          # Train model (10 epochs)
make train-full     # Full training (20 epochs, batch 64)
make train-quick    # Quick training (3 epochs)
make train-custom EXAMPLES=path EPOCHS=20
```

### Training via Script

```bash
# Basic training
python scripts/train_model.py --examples examples/10000_examples.pyrl

# With parameters
python scripts/train_model.py \
    --examples examples/10000_examples.pyrl \
    --epochs 20 \
    --batch-size 64 \
    --learning-rate 0.0001 \
    --hidden-size 768 \
    --layers 12

# From examples directory
python scripts/train_model.py --examples-dir examples/
```

### Training Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--examples` | - | Path to examples file |
| `--examples-dir` | - | Path to examples directory |
| `--output` | models/pyrl-model | Output model directory |
| `--epochs` | 10 | Number of training epochs |
| `--batch-size` | 32 | Batch size |
| `--learning-rate` | 0.0001 | Learning rate |
| `--max-length` | 512 | Maximum sequence length |
| `--hidden-size` | 768 | Hidden layer size |
| `--layers` | 12 | Number of transformer layers |
| `--heads` | 12 | Number of attention heads |

### Pyrl Tokenizer

Pyrl uses a specialized tokenizer with support for:

**Special Tokens:**
- `<pad>`, `<unk>`, `<bos>`, `<eos>`, `<mask>`
- `<newline>`, `<indent>`, `<dedent>`

**Sigils:**
- `$` (scalar), `@` (array), `%` (hash), `&` (function)

**Keywords:**
- `if`, `elif`, `else`, `while`, `for`, `in`, `def`, `return`, `class`, `lambda`, etc.

**Operators:**
- `+`, `-`, `*`, `/`, `**`, `//`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `=`, etc.

**Built-in Functions:**
- `print`, `len`, `range`, `str`, `int`, `float`, `list`, `dict`, etc.

### Training Results

| Metric | Value |
|--------|-------|
| Examples | 334 |
| Tokens | 13,898 |
| Vocabulary | 1,778 |
| Val Loss | 0.70 |

### Checkpoints

During training, checkpoints are saved:

```
checkpoints/
├── checkpoint_epoch_1.json
├── checkpoint_epoch_2.json
└── ...
```

Each checkpoint contains:
- Epoch number
- Validation loss
- Vocabulary size
- Timestamp

---

## API Server

### Starting the Server

```bash
# Development mode
python pyrl_server.py

# Via uvicorn
uvicorn pyrl_server:app --host 0.0.0.0 --port 8000
```

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Server info |
| GET | `/health` | Health check |
| POST | `/execute` | Execute code |
| POST | `/tokenize` | Tokenize code |
| POST | `/parse` | Parse to AST |
| POST | `/reset` | Reset VM |
| GET | `/variables` | Get variables |
| GET | `/plugins` | Loaded plugins |
| POST | `/plugins/load` | Load a plugin |
| GET | `/config` | Configuration |
| GET | `/stats` | Server statistics |

### Request Examples

**Execute code:**

```bash
curl -X POST http://localhost:8000/execute \
    -H "Content-Type: application/json" \
    -d '{"code": "$x = 10\nprint($x)"}'
```

**Response:**

```json
{
    "success": true,
    "result": null,
    "output": "10\n",
    "variables": {"x": 10}
}
```

**Tokenize:**

```bash
curl -X POST http://localhost:8000/tokenize \
    -H "Content-Type: application/json" \
    -d '{"code": "$x = 10"}'
```

---

## Docker

### Available Images

| Image | Description |
|-------|-------------|
| `Dockerfile.server` | API server |
| `Dockerfile.console` | CLI console |
| `Dockerfile.dev` | Development environment |
| `Dockerfile.training` | Model training |
| `Dockerfile.model-generator` | Model generation |
| `Dockerfile.model-inference` | Model inference |

### Build and Run

```bash
# Build all images
make docker-build

# Run server
make docker-run-server

# Run via docker-compose
make docker-up
```

### Docker Compose

```yaml
services:
  pyrl-server:
    build:
      context: .
      dockerfile: docker/Dockerfile.server
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
```

---

## Language Grammar *(NEW v2.2)*

Pyrl uses a Lark parser with a formal LALR grammar. The grammar is defined in `src/core/lark_parser.py`.

### Core Rules

```
start: (_NL | statement)*

statement: simple_stmt _NL?
         | compound_stmt

simple_stmt: return_statement
           | assignment
           | print_statement
           | expression_statement

compound_stmt: function_definition
             | class_definition
             | conditional
             | loop
```

### Variables with Sigils

```
SCALAR_VAR: "$" IDENT    # $name - scalar
ARRAY_VAR: "@" IDENT     # @items - array
HASH_VAR: "%" IDENT      # %data - hash
FUNC_VAR: "&" IDENT      # &func - function
```

### Operators

```
COMP_OP: "==" | "!=" | "<=" | ">=" | "=~" | "!~" | "<" | ">"
ADD_OP: "+" | "-"
MUL_OP: "//" | "*" | "/" | "%"
POW_OP: "**" | "^"
```

### Keywords

```
if, elif, else, while, for, in, def, return, class, extends,
method, init, prop, test, print, assert, and, or, not, True, False, None
```

### Functions

```
function_definition: DEF IDENT "(" [arg_list] ")" ":" _NL INDENT statement+ DEDENT
func_var_definition: FUNC_VAR "(" [arg_list] ")" "=" block
```

### Classes

```
class_definition: CLASS IDENT [EXTENDS IDENT] "{" class_member* "}"
class_member: method_def | property_def
method_def: METHOD IDENT "(" [arg_list] ")" "=" block
property_def: PROP IDENT ["=" expression]
```

### Control Flow

```
conditional: IF expression ":" _NL INDENT statement+ DEDENT else_clause?
loop: FOR SCALAR_VAR IN expression ":" _NL INDENT statement+ DEDENT
    | WHILE expression ":" _NL INDENT statement+ DEDENT
```

### Model Training with Grammar

The `scripts/train_model.py` script uses grammar for feature extraction:

```bash
# Train with grammar features
python scripts/train_model.py --examples-dir examples/

# Without grammar features
python scripts/train_model.py --no-grammar
```

Extracted features:
- AST node types
- Sigil usage ($, @, %, &)
- Keyword frequency
- Operator frequency
- Parse success rate

---

## Examples

### Factorial

```pyrl
def factorial($n):
    if $n <= 1:
        return 1
    return $n * factorial($n - 1)

$result = factorial(5)  # 120
```

### Fibonacci Numbers

```pyrl
def fibonacci($n):
    if $n <= 1:
        return $n
    return fibonacci($n - 1) + fibonacci($n - 2)

for $i in range(10):
    print(fibonacci($i))
```

### Bubble Sort

```pyrl
def bubble_sort(@arr):
    $n = len(@arr)
    for $i in range($n):
        for $j in range($n - $i - 1):
            if @arr[$j] > @arr[$j + 1]:
                $temp = @arr[$j]
                @arr[$j] = @arr[$j + 1]
                @arr[$j + 1] = $temp
    return @arr

@sorted = bubble_sort([64, 34, 25, 12, 22, 11, 90])
```

### HTTP Request

```pyrl
$response = http_get("https://api.example.com/data")
if $response{"status"} == 200:
    $data = json_parse($response{"data"})
    print($data)
```

---

## Web Server with Authentication

A complete web application example in Pyrl with frontend and backend is available at `examples/web_server_auth.pyrl`.

### Application Structure

```pyrl
# Server configuration
%config = {
    host: "0.0.0.0",
    port: 8080,
    secret_key: "pyrl_secret_key_2024",
    session_timeout: 3600
}

# User database (in-memory)
%users = {
    "admin": {password: "admin123", role: "administrator", name: "Administrator"},
    "user": {password: "user123", role: "user", name: "Regular User"}
}

# Session storage
%sessions = {}
```

### HTTP Server Class

```pyrl
class PyrlServer:
    def __init__($self, %config):
        $self.host = %config{host}
        $self.port = %config{port}
        $self.routes = {}
    
    def route($self, $path, $method, &handler):
        $key = $method + ":" + $path
        %{$self.routes}{$key} = &handler
    
    def handle_request($self, $method, $path, %headers, $body):
        $key = $method + ":" + $path
        if $key in $self.routes:
            $handler = $self.routes{$key}
            return $handler(%headers, $body)
        return $self.error_response(404, "Not Found")
```

### Application Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Login page |
| POST | `/login` | Process authentication |
| GET | `/dashboard` | Admin dashboard (requires auth) |
| POST | `/logout` | Logout user |
| GET | `/api/status` | API status endpoint |

### Authentication Function

```pyrl
def verify_user($username, $password):
    if $username in %users:
        $user = %users{$username}
        if $user{password} == $password:
            return {success: True, user: $user}
    return {success: False, error: "Invalid credentials"}

def create_session($username):
    $token = generate_token($username)
    %sessions{$token} = {
        username: $username,
        created: time(),
        expires: time() + %config{session_timeout}
    }
    return $token
```

### Login Handler

```pyrl
def handle_login_post(%headers, $body):
    # Parse form data
    @params = split($body, "&")
    %form_data = {}
    for $param in @params:
        @parts = split($param, "=")
        %form_data{@parts[0]} = @parts[1]
    
    $username = %form_data{username}
    $password = %form_data{password}
    
    # Verify credentials
    $result = verify_user($username, $password)
    
    if $result{success}:
        $token = create_session($username)
        return {
            status: 302,
            headers: {
                "Location": "/dashboard",
                "Set-Cookie": "session=" + $token
            },
            body: ""
        }
    else:
        return {
            status: 302,
            headers: {"Location": "/?error=1"},
            body: ""
        }
```

### HTML Templates (Frontend)

**Login Page:**
- Form with username and password fields
- Error display for invalid credentials
- Modern CSS styling

**Dashboard:**
- Welcome message with user name
- Statistics (users, posts, views)
- Activity history
- Quick actions

### Running the Server

```bash
# Execute the example
python pyrl_cli.py examples/web_server_auth.pyrl

# Or via REPL
pyrl> run examples/web_server_auth.pyrl
```

### Test Credentials

| Login | Password | Role |
|-------|----------|------|
| admin | admin123 | Administrator |
| user | user123 | Regular User |
| guest | guest123 | Guest User |

### Authentication Flow

```
1. GET /               → Display login form
2. POST /login         → Verify credentials
   ├─ Success          → Create session, redirect /dashboard
   └─ Failed           → Redirect /?error=1
3. GET /dashboard      → Check session
   ├─ Valid session    → Display dashboard
   └─ Invalid/None     → Redirect /
4. POST /logout        → Remove session, redirect /
```

---

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `True` | `True` | Boolean true |
| `False` | `False` | Boolean false |
| `None` | `None` | Null value |
| `PI` | 3.141592653589793 | π constant |
| `E` | 2.718281828459045 | e constant |
| `INF` | `float('inf')` | Infinity |
| `NAN` | `float('nan')` | Not a Number |

---

## License

MIT License

---

**Pyrl Team**  
Repository: http://178.140.10.58:8082/ai/pyrl-project.git
