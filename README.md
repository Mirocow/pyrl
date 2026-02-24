<p align="center">
  <img src="docs/images/pyrl_banner.png" alt="Pyrl Banner" width="100%">
</p>

<p align="center">
  <img src="docs/images/pyrl_logo.png" alt="Pyrl Logo" width="150">
</p>

<h1 align="center">Pyrl — Hybrid Python + Perl Programming Language</h1>

<p align="center">
  <strong>Power of Perl. Simplicity of Python. One Language.</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-documentation">Documentation</a> •
  <a href="#-examples">Examples</a> •
  <a href="#-tools">Tools</a>
</p>

<p align="center">
  <strong>English</strong> | <a href="README_RU.md">Русский</a>
</p>

---

## 🎯 About

**Pyrl** (Python + Perl) is a modern hybrid programming language that combines Perl's expressive power with Python's readability and simplicity. The language uses Perl's sigil-based variable system (`$scalar`, `@array`, `%hash`, `&function`) together with Python's control flow syntax and indentation.

### Key Features

- 🔥 **Sigil Variables** — intuitive type recognition by prefix
- 🐍 **Python Syntax** — familiar `if`, `for`, `while`, `def` constructs
- 🐪 **Perl Power** — regular expressions, built-in operators
- 🗄️ **SQLite Integration** — native database operations
- 🌐 **Web Server** — built-in HTTP server with REST API
- 🤖 **AI Model** — pretrained model for code generation

---

## ✨ Features

### Sigil-Based Variables

```pyrl
$name = "Pyrl"          # Scalar ($)
@numbers = [1, 2, 3]    # Array (@)
%config = {             # Hash (%)
    "host": "localhost",
    "port": 8080
}
&handler = {            # Function (&)
    return "Hello!"
}
```

### Python-Like Syntax

```pyrl
def greet($name):
    if $name:
        return "Hello, " + $name + "!"
    else:
        return "Hello, World!"

for $i in range(5):
    print($i)
```

### Perl-Style Regular Expressions

```pyrl
$text = "Hello, World!"
if $text =~ m/World/:
    print("Found!")

$result = $text =~ s/World/Pyrl/
```

### Web Applications

```pyrl
$app = {
    handle: &handle_request
}

def handle_request($req):
    %response = {
        "status": 200,
        "body": "Hello from Pyrl!"
    }
    return %response
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/pyrl-lang/pyrl.git
cd pyrl

# Install dependencies
pip install -r requirements.txt
```

### Running

```bash
# Interactive console
python pyrl_cli.py

# Execute file
python pyrl_cli.py examples/01_hello_world.pyrl

# Web server
python scripts/run_web_app.py examples/web_server_auth.pyrl
```

### Docker

```bash
# Start server
docker-compose up -d server

# Console
docker-compose run console
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [**Language Documentation (EN)**](documents/DOCUMENTATION_EN.md) | Complete syntax and features reference |
| [**Документация языка (RU)**](documents/DOCUMENTATION_RU.md) | Полное описание синтаксиса и возможностей |
| [**VSCode Extension**](documents/VSCODE_PLUGIN.md) | Extension installation and usage |
| [**AI Model**](documents/AI_MODEL.md) | Model training and inference |
| [**Docker Services**](docker/README.md) | Containerization and deployment |
| [**Project Roadmap**](PROJECT_ROADMAP.md) | Development plans |
| [**CHANGELOG**](CHANGELOG.md) | Version history |

---

## 🛠️ Tools

### VSCode Extension

Plugin for Visual Studio Code with syntax highlighting, autocompletion, and snippets.

```bash
cd vscode-pyrl
code --install-extension .
```

**Features:**
- 🎨 Syntax highlighting
- 📝 Quick construction snippets
- 🔍 Variable autocompletion

### AI Model Generator

Train your own model for Pyrl code generation:

```bash
# Generate model
python scripts/generate_model.py

# Training
python scripts/train_model.py --epochs 10

# Inference
python scripts/model_inference.py
```

### Pretrained Model

The repository includes a pretrained model:
- **Location:** `models/pyrl-model/`
- **Tokenizer:** BPE, 10,000 tokens
- **Architecture:** Transformer-based

---

## 📁 Project Structure

```
pyrl/
├── src/
│   └── core/
│       ├── lark_parser.py      # LALR parser
│       └── vm/
│           ├── vm.py           # Virtual machine
│           ├── builtins.py     # Built-in functions
│           ├── builtins_db.py  # SQLite functions
│           └── builtins_http.py # HTTP functions
├── vscode-pyrl/                # VSCode extension
├── scripts/
│   ├── generate_model.py       # Model generator
│   └── train_model.py          # Model training
├── models/pyrl-model/          # Pretrained model
├── examples/                   # Code examples
├── docker/                     # Docker configs
└── documents/                  # Documentation
```

---

## 📋 Examples

| File | Description |
|------|-------------|
| [01_hello_world.pyrl](examples/01_hello_world.pyrl) | Hello World |
| [01_variables.pyrl](examples/01_variables.pyrl) | Variables |
| [04_functions.pyrl](examples/04_functions.pyrl) | Functions |
| [06_classes.pyrl](examples/06_classes.pyrl) | Classes |
| [08_builtins.pyrl](examples/08_builtins.pyrl) | Built-in functions |
| [20_perl_regex.pyrl](examples/20_perl_regex.pyrl) | Regular expressions |
| [web_server_auth.pyrl](examples/web_server_auth.pyrl) | Auth web server |

---

## 🧪 Testing

```bash
# Run all tests
make test

# Specific test
python -m pytest tests/test_vm.py -v
```

---

## 🗺️ Roadmap

See [PROJECT_ROADMAP.md](documents/PROJECT_ROADMAP.md) for development plans.

### Current Version: 2.3.0

- ✅ SQLite integration
- ✅ Web server with REST API
- ✅ AI model for code generation
- ✅ VSCode extension

### Planned

- 🔄 JIT compilation
- 🔄 Standard library
- 🔄 Package manager
- 🔄 Debugger

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repository
2. Create a branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📄 License

MIT License — use freely for any purpose.

---

<p align="center">
  <strong>Pyrl</strong> — bringing the best of Python and Perl together
</p>
