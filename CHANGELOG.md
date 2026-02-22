# Changelog

All notable changes to the Pyrl project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-02-22

### Added
- **Complete rewrite of the interpreter** with AST-based architecture
- **Plugin system** (`pyrl_plugin_system.py`) for extending functionality
- **5 built-in plugins**:
  - `math_extended`: sqrt, pow, sin, cos, tan, pi, e, floor, ceil
  - `datetime`: now, today, format_date, date_add, timestamp
  - `http_client`: http_get, http_post, http_put, http_delete
  - `crypto`: md5, sha256, base64_encode, uuid, random_string
  - `collections`: flatten, unique, intersection, chunk, find
- **AI Assistant** (`pyrl_ai.py`) for code generation
- **Training data generator** (`data_generator.py`) with 32 examples
- **OOP extension** (`pyrl_oop_plugin.py`, `pyrl_vm_extended.py`)
  - Class definitions with `class` keyword
  - Inheritance with `extends` keyword
  - Constructors with `init` method
  - Instance methods with `method` keyword
  - Properties with `prop` keyword
- **VSCode extension** with syntax highlighting and snippets
- **Docker support** with multi-stage builds
  - Production image
  - Development image
  - Training image (GPU support)
  - API server image
- **Comprehensive test suite** with 272 tests (89% pass rate)
  - Parser tests (87)
  - AST builder tests (37)
  - Interpreter tests (60)
  - Built-in functions tests (46)
  - Vue generator tests (19)
  - Integration tests (23)

### Changed
- Migrated from Transformer-based execution to AST-based interpreter
- Improved error handling with custom exception classes
- Better variable scoping in functions
- Enhanced regex support with proper escape handling

### Fixed
- Conditional execution (both branches were executing)
- Return statements in functions
- Hash access syntax (`%hash["key"]`)
- Array index auto-extension
- Comment handling in strings
- Unicode escape sequences in strings

## [1.0.0] - 2024-01-15

### Added
- Initial release of Pyrl Virtual Machine
- Sigil-based variables ($scalar, @array, %hash, &function)
- Lark parser with Earley algorithm
- Basic interpreter with statement execution
- Built-in test framework with assertions
- Vue.js 3 component generation
- Regex operators (=~, !~)
- HTTP server support
- Basic documentation

### Core Features
- Variable types: scalars, arrays, hashes, functions
- Control flow: if-else, for loops, while loops
- Operators: arithmetic, comparison, logical, regex
- Functions: definition, parameters, return values
- Testing: test blocks, assertions

## [0.9.0] - 2024-01-01

### Added
- Proof of concept interpreter
- Basic grammar definition
- Simple variable assignment
- Print statement

---

## Roadmap

### [2.1.0] - Planned
- [ ] Async/await support
- [ ] Module system
- [ ] Package manager
- [ ] Improved error messages with source location
- [ ] Debugger integration

### [2.2.0] - Planned
- [ ] Type hints
- [ ] Pattern matching
- [ ] Macro system
- [ ] WebAssembly compilation

### [3.0.0] - Future
- [ ] Self-hosting compiler
- [ ] IDE integration
- [ ] Package registry
- [ ] Community plugins
