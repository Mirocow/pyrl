# Changelog

All notable changes to the Pyrl language will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-02-24

### Added

#### Real HTTP Server Support
- **NEW**: `examples/web_server_auth.pyrl` now creates a fully functional HTTP server
- Beautiful login page with gradient UI and error handling
- Dashboard with user information and statistics after successful login
- Session management with cookies and token validation
- REST API endpoints for external integrations

#### Web Server Example (`examples/app.pyrl`)
- Simple application server template with business logic in pyrl file
- CRUD operations example with in-memory data storage
- Clean separation of configuration, data, business logic, and HTTP handler

### Changed

#### `examples/web_server_auth.pyrl`
- Complete rewrite to work as real HTTP server (not just demonstration)
- Added `$app` export for `run_web_app.py` wrapper
- Added `check_login()` helper function for cleaner authentication logic
- Fixed session validation and cookie handling

### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/status` | Server status |
| GET | `/api/users` | List all users |
| GET | `/api/user/{name}` | Get user info |
| POST | `/api/verify` | Verify credentials (JSON) |
| POST | `/api/validate` | Validate session token |
| POST | `/api/logout` | Logout (API) |

### Running the Server

```bash
cd /home/z/my-project/pyrl
python scripts/run_web_app.py --file examples/web_server_auth.pyrl --port 8080
```

### Test Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| user | user123 | User |
| guest | guest123 | Guest |

## [2.0.0] - 2025-01-10

### Added

#### Anonymous Functions
- **NEW**: Anonymous function syntax with block body: `&name($params) = { body }`
- Block syntax for function bodies with semicolon-separated statements
- Control flow inside blocks: `if/while/for` with block syntax
- Function references can be stored in variables: `$func = &my_function`
- Nested function calls work correctly

```pyrl
&reverse_string($str) = {
    $reversed = "";
    $len = len($str);
    $i = $len - 1;
    while $i >= 0 {
        $reversed = $reversed + $str[$i];
        $i = $i - 1
    };
    return $reversed
}

$func = &reverse_string
print($func("hello"))  # "olleh"
```

#### OOP Support
- **NEW**: Class definition syntax: `class Name [extends Parent] { members }`
- **NEW**: Method definition: `method name(params) = { body }`
- **NEW**: Constructor: `init(params) = { body }`
- **NEW**: Property definition: `prop name [= value]`
- **NEW**: Method calls on instances: `$obj.method(args)`

```pyrl
class Person {
    prop name = "Unknown"
    prop age = 0
    
    init($name, $age) = {
        $name = $name;
        $age = $age
    }
    
    method get_name() = {
        return $name
    }
}

$p = Person("Alice", 30)
print($p.get_name())  # "Alice"
```

#### Block Syntax
- Block statements enclosed in `{ }`
- Statements separated by `;`
- Control flow inside blocks: `if expr { }`, `while expr { }`, `for $var in expr { }`

### Fixed

#### Variable Shadowing
- Variables are now stored with sigil prefixes (`$`, `@`, `%`, `&`)
- Prevents shadowing of built-in functions like `len`, `lower`, `type`, etc.

```pyrl
# Before: this would break len()
$len = 5

# Now: $len stored as '$len', 'len' function still works
print(len("hello"))  # 5
```

#### Function Parameter Binding
- Function parameters are properly prefixed with `$`
- Nested function calls work correctly
- Recursive functions work correctly

### Changed

#### Internal Architecture
- Variable storage uses prefixed names internally
- `get_variable()` and `has_variable()` methods handle prefix lookup
- Function calls try `&` prefix for user-defined functions first

#### Parser
- Added `func_var_definition` rule for `&name():` and `&name() = {}` syntax
- Added `block`, `block_stmts`, `block_stmt` rules
- Added `block_if`, `block_while`, `block_for` rules
- Added `class_definition`, `class_body`, `class_member` rules
- Added `method_def`, `property_def`, `method_call` rules

### Tests
- All 321 tests passing
- Added tests for anonymous functions
- Added tests for OOP features
- Updated tests for new variable storage format

## [1.1.0] - 2025-01-09

### Changed

#### Architecture
- **BREAKING**: Removed legacy lexer, parser, interpreter modules - now using Lark parser exclusively
- Deleted files: `lexer.py`, `parser.py`, `interpreter.py`, `ast_nodes.py`, `builtins.py`
- Deleted tests: `test_lexer.py`, `test_parser.py`
- Updated `__init__.py` to export only Lark-based components

#### Grammar
- **BREAKING**: Unified index access syntax - both arrays and hashes now use `[]` brackets (Python-style)
  - Before: `%person{"name"}` (curly braces)
  - After: `%person["name"]` (square brackets)
- Simplified grammar with `index_access` rule that handles both array and hash indexing
- Improved error reporting with detailed line numbers and context

#### Parser
- Added `index_access` transformer method
- Improved `IdentRef` handling for built-in functions
- Better function definition parsing with support for both `def name()` and `&name()` syntaxes

#### Examples
- Updated all examples to use `[]` for hash access instead of `{}`
- Fixed `02_variables.pyrl` to use correct syntax
- Fixed `05_arrays_hashes.pyrl` to use correct syntax
- Fixed `10000_examples.pyrl` to use correct syntax
- Fixed `web_server_auth.pyrl` to use correct syntax

#### Tests
- Updated `conftest.py` to use Lark-based VM as primary implementation
- Added `parser` fixture for Lark parser tests
- Added `lark` test marker
- Removed legacy lexer and parser tests

### Added
- Created `README.md` with project overview and quick start guide
- Created `CHANGELOG.md` for version tracking

### Fixed
- Hash access now works consistently with array access
- Function calls with built-in functions (str, len, int, etc.) work correctly
- All imports from `src` and `src.core` work correctly with Lark-based components

## [1.0.0] - 2024

### Added
- Initial release of Pyrl language
- Sigil-based variables: `$scalar`, `@array`, `%hash`, `&function`
- Python-style indentation syntax
- Lark-based parser with EBNF grammar
- Virtual Machine (VM) for code execution
- Built-in functions:
  - Type conversion: `int`, `float`, `str`, `bool`, `list`, `dict`
  - Math: `abs`, `round`, `min`, `max`, `sum`, `pow`, `sqrt`, `sin`, `cos`, `tan`, `log`, `exp`, `floor`, `ceil`
  - String: `lower`, `upper`, `strip`, `split`, `join`, `replace`, `find`, `startswith`, `endswith`
  - List: `append`, `extend`, `insert`, `remove`, `pop`, `index`, `count`, `sort`, `reverse`
  - Dict: `keys`, `values`, `items`, `get`, `setdefault`, `update`, `popitem`
  - Random: `random`, `randint`, `choice`, `shuffle`, `seed`
  - Utility: `enumerate`, `zip`, `map`, `filter`, `sorted`, `reversed`, `any`, `all`
  - Regex: `re_match`, `re_search`, `re_findall`, `re_sub`, `re_split`
  - HTTP/JSON: `http_get`, `http_post`, `json_parse`, `json_stringify`
  - Time: `time`, `sleep`
- Control flow: `if/elif/else`, `for`, `while`
- Functions with parameters and return values
- Recursion support
- Test blocks with `test` keyword
- Vue component generation
- API server with FastAPI
- CLI tool for running .pyrl files
- Docker configuration for deployment
- ML model training capabilities

### Documentation
- Russian documentation (DOCUMENTATION_RU.md)
- English documentation (DOCUMENTATION_EN.md)
- Multiple example files demonstrating language features

### Tests
- VM tests
- Integration tests
