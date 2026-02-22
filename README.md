# Pyrl Ecosystem

**Version 2.0.0** | Hybrid Python-Perl Inspired Language with AI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: 89%](https://img.shields.io/badge/tests-89%25-green.svg)]()

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/pyrl-ecosystem/pyrl.git
cd pyrl-project
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Try the CLI
python pyrl_cli.py repl
```

## 📁 Project Structure

```
pyrl-project/
├── src/                         # Source code
│   ├── pyrl_vm.py              # Main interpreter
│   ├── pyrl_plugin_system.py   # Plugin architecture
│   ├── pyrl_oop_plugin.py      # OOP extension
│   ├── pyrl_vm_extended.py     # VM with classes
│   ├── pyrl_ai.py              # AI assistant
│   └── data_generator.py       # Training data generator
│
├── plugins/                     # Built-in plugins
│   ├── math_extended/          # Math: sqrt, sin, cos, pi, e
│   ├── datetime/               # Dates: now, format_date
│   ├── http_client/            # HTTP: get, post, put, delete
│   ├── crypto/                 # Crypto: sha256, uuid, base64
│   └── collections/            # Arrays: flatten, unique, chunk
│
├── models/                      # AI model
│   ├── README.md               # Model documentation
│   └── training_metadata.json  # Training info
│
├── training/                    # Training pipeline
│   ├── dataset.jsonl           # 32 training examples
│   ├── train_model.py          # Training script
│   └── train_config.yaml       # Configuration
│
├── tests/                       # Test suite (272 tests)
│   ├── test_parser.py          # Parser tests (87)
│   ├── test_ast_builder.py     # AST tests (37)
│   ├── test_interpreter.py     # Interpreter tests (60)
│   ├── test_builtins.py        # Built-ins tests (46)
│   ├── test_vue_generator.py   # Vue tests (19)
│   └── test_integration.py     # Integration tests (23)
│
├── examples/                    # Example programs
│   ├── auth/auth_app.pyrl      # Auth system
│   ├── oop/oop_examples.pyrl   # OOP examples
│   └── algorithms/algorithms.pyrl
│
├── docs/                        # Documentation
│   ├── DOCUMENTATION.md        # Full docs
│   └── EXTENDING_PYRL.md       # Extension guide
│
├── docker/                      # Docker
│   ├── Dockerfile              # Multi-stage build
│   └── api_server.py           # FastAPI server
│
├── vscode-extension/            # VSCode extension
│   ├── syntaxes/pyrl.tmLanguage.json
│   ├── snippets/pyrl-snippets.json
│   └── package.json
│
├── pyrl_cli.py                  # Command-line interface
├── Makefile                     # Build commands
├── pyproject.toml              # Project config
├── requirements.txt            # Dependencies
├── CHANGELOG.md                # Version history
├── LICENSE                     # MIT
└── README.md                   # This file
```

## 📦 Components

### 1. Interpreter (`src/pyrl_vm.py`)

- Sigil-based variables: `$scalar`, `@array`, `%hash`, `&function`
- Regex operators: `=~`, `!~`
- Built-in test framework
- Vue.js 3 component generation
- 272 tests, 89% pass rate

### 2. Plugin System (`src/pyrl_plugin_system.py`)

5 built-in plugins with 30+ functions:

| Plugin | Functions |
|--------|-----------|
| math_extended | sqrt, pow, sin, cos, tan, pi, e, floor, ceil |
| datetime | now, today, format_date, date_add, timestamp |
| http_client | http_get, http_post, json_parse |
| crypto | md5, sha256, base64_encode, uuid |
| collections | flatten, unique, intersection, chunk |

### 3. AI Assistant (`src/pyrl_ai.py`)

- Code generation from natural language
- Code explanation
- Error fixing
- Plugin suggestions

### 4. OOP Extension (`src/pyrl_vm_extended.py`)

```pyrl
class User {
    prop name = ""
    
    init($name) = {
        @self.name = $name
    }
    
    method greet() = {
        return "Hello, " + @self.name
    }
}

$admin = Admin("Alice", "admin@example.com")
print($admin.greet())
```

### 5. Training Pipeline (`training/`)

- 32 training examples in JSONL format
- SFT training with LoRA
- GPU support via Docker

## 🐳 Docker

```bash
# Build all images
make docker-build

# Production
docker run -it pyrl:latest

# API server
docker run -p 8000:8000 pyrl:api

# Development
make docker-dev

# Training (GPU)
docker build -f docker/Dockerfile --target training -t pyrl:training .
docker run --gpus all pyrl:training
```

## 🧪 Testing

```bash
# Run all tests
make test

# With coverage
make test-cov

# Output: 272 tests, 89% passed
```

## 📖 Documentation

- [Full Documentation](docs/DOCUMENTATION.md)
- [Extending Pyrl](docs/EXTENDING_PYRL.md)
- [CHANGELOG](CHANGELOG.md)

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Source Files | 15 Python files |
| Plugins | 5 built-in |
| Tests | 272 (89% pass) |
| Training Examples | 32 |
| Lines of Code | ~8,000 |

## 🔧 Commands

```bash
make install      # Install dependencies
make test         # Run tests
make lint         # Lint code
make format       # Format code
make train        # Train AI model
make docker-build # Build Docker images
```

## 📜 License

MIT License - See [LICENSE](LICENSE)

---

**Pyrl Ecosystem Team** | 2024
