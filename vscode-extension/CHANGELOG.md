# Changelog

All notable changes to the "Pyrl Language Support" extension will be documented in this file.

## [1.0.0] - 2024-01-15

### Added
- Initial release
- Syntax highlighting for all Pyrl constructs:
  - Scalar (`$`), array (`@`), hash (`%`), and function (`&`) variables
  - Keywords: if, else, for, while, return, test, assert, vue
  - Strings: double-quoted and single-quoted
  - Regex literals: `r"pattern"`
  - Numbers: integers, floats, hex, binary
  - Operators: arithmetic, comparison, logical, regex
  - Comments: single-line with `#`
- Code snippets for common patterns
- Language configuration:
  - Bracket matching
  - Auto-closing pairs
  - Comment toggling
  - Indentation rules
- Vue component generation syntax support

### Features
- Full sigil-based variable highlighting with distinct colors
- Regex pattern syntax highlighting within `r"..."` strings
- Test block support with assertion highlighting
- Vue component definition highlighting

## [0.1.0] - 2024-01-01

### Added
- Basic syntax highlighting prototype
- Initial grammar definition
