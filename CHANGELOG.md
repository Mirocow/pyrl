# Changelog

All notable changes to the Pyrl language will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
