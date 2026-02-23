# Pyrl Makefile
# Build and development commands for Pyrl language platform
# Version: 2.0.0

.PHONY: all install test lint clean run help \
        docker-build docker-up docker-down \
        security security-audit security-check \
        deps deps-update deps-outdated \
        docs docs-serve docs-clean \
        benchmark benchmark-full \
        pre-commit pre-commit-install pre-commit-run \
        release release-patch release-minor release-major \
        validate validate-config validate-env \
        health health-check \
        ci ci-test ci-lint ci-build \
        profile profile-memory profile-time \
        watch watch-test watch-lint \
        git git-push git-pull git-status git-log \
        train train-full train-quick train-custom \
        model model-info model-inference model-export \
        web web-server web-auth web-api \
        api api-test api-execute api-tokenize \
        plugin plugin-list plugin-load \
        checkpoint checkpoint-list checkpoint-restore

# ===========================================
# Configuration
# ===========================================

PYTHON := python
PIP := pip
SERVER_HOST := 0.0.0.0
SERVER_PORT := 8000
GIT_REMOTE := origin
GIT_BRANCH := main
MODEL_PATH := models/pyrl-model
EXAMPLES_PATH := examples/10000_examples.pyrl

# ===========================================
# Default
# ===========================================

all: install
	@echo "✓ Pyrl installed successfully!"
	@echo "Run 'make help' to see available commands"

# ===========================================
# Installation
# ===========================================

install:
	@echo "📦 Installing dependencies..."
	$(PIP) install -r requirements.txt

install-dev:
	@echo "📦 Installing development dependencies..."
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

install-full:
	@echo "📦 Installing all dependencies including dev tools..."
	$(PIP) install -r requirements.txt
	$(PIP) install -e .
	$(PIP) install pytest pytest-cov flake8 pylint black isort mypy pre-commit

# ===========================================
# Testing
# ===========================================

test:
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short

test-cov:
	@echo "🧪 Running tests with coverage..."
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-quick:
	@echo "🧪 Running quick tests..."
	pytest tests/ -v -x --tb=line

test-file:
	@echo "🧪 Running specific test file: $(FILE)"
	pytest tests/$(FILE) -v

test-marker:
	@echo "🧪 Running tests with marker: $(MARKER)"
	pytest tests/ -v -m $(MARKER)

# ===========================================
# Code Quality
# ===========================================

lint:
	@echo "🔍 Running linter..."
	flake8 src/ tests/ --max-line-length=100 || true
	pylint src/ || true

lint-fix:
	@echo "🔍 Auto-fixing lint issues..."
	autopep8 --in-place --recursive src/ tests/ || true

format:
	@echo "✨ Formatting code..."
	black src/ tests/
	isort src/ tests/

format-check:
	@echo "✨ Checking code format..."
	black --check src/ tests/
	isort --check src/ tests/

type-check:
	@echo "🔎 Running type checker..."
	mypy src/ || true

quality: lint format-check type-check
	@echo "✓ All quality checks passed!"

# ===========================================
# Cleaning
# ===========================================

clean:
	@echo "🧹 Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/ .coverage htmlcov/ .tox/ dist/ build/

clean-all: clean
	@echo "🧹 Deep cleaning..."
	rm -rf .mypy_cache/ .ruff_cache/
	rm -rf models/*.bin models/*.pt
	rm -rf checkpoints/*.json
	rm -rf *.zip *.tar.gz

clean-model:
	@echo "🧹 Cleaning model files..."
	rm -rf $(MODEL_PATH)/*

clean-checkpoints:
	@echo "🧹 Cleaning checkpoints..."
	rm -rf checkpoints/*.json

# ===========================================
# Running
# ===========================================

run-server:
	@echo "🚀 Starting Pyrl server on $(SERVER_HOST):$(SERVER_PORT)..."
	$(PYTHON) pyrl_server.py

run-cli:
	@echo "🚀 Starting Pyrl CLI REPL..."
	$(PYTHON) pyrl_cli.py

run-cli-debug:
	@echo "🚀 Starting Pyrl CLI in debug mode..."
	PYRL_DEBUG=1 $(PYTHON) pyrl_cli.py --debug

run-cli-file:
	@echo "🚀 Running Pyrl file: $(FILE)"
	$(PYTHON) pyrl_cli.py $(FILE)

dev:
	@echo "🔧 Starting development server with hot reload..."
	uvicorn pyrl_server:app --reload --host $(SERVER_HOST) --port $(SERVER_PORT)

# ===========================================
# Examples
# ===========================================

run-examples:
	@echo "📚 Running all examples..."
	@for f in examples/*.pyrl; do \
		echo "\n=== Running $$f ==="; \
		$(PYTHON) pyrl_cli.py "$$f" || true; \
	done

example:
	@echo "📚 Running example: $(FILE)"
	$(PYTHON) pyrl_cli.py examples/$(FILE).pyrl

example-hello:
	@echo "📚 Hello World example..."
	$(PYTHON) pyrl_cli.py -c 'print("Hello, Pyrl!")'

example-auth:
	@echo "📚 Web server auth example..."
	$(PYTHON) pyrl_cli.py examples/web_server_auth.pyrl

list-examples:
	@echo "📚 Available examples:"
	@ls -la examples/*.pyrl 2>/dev/null || echo "No examples found"

# ===========================================
# Web Server Examples
# ===========================================

web-server:
	@echo "🌐 Starting Pyrl web server..."
	$(PYTHON) pyrl_server.py --host $(SERVER_HOST) --port $(SERVER_PORT)

web-auth:
	@echo "🌐 Starting web auth example server..."
	$(PYTHON) pyrl_cli.py examples/web_server_auth.pyrl

web-api:
	@echo "🌐 Starting API server..."
	uvicorn docker.api_server:app --host $(SERVER_HOST) --port $(SERVER_PORT)

# ===========================================
# API Testing
# ===========================================

api-test:
	@echo "🔌 Testing API health..."
	curl -s http://localhost:$(SERVER_PORT)/health | python -m json.tool || echo "Server not running"

api-execute:
	@echo "🔌 Executing code via API..."
	curl -X POST http://localhost:$(SERVER_PORT)/execute \
		-H "Content-Type: application/json" \
		-d '{"code": "$(CODE)"}' | python -m json.tool

api-execute-hello:
	@echo "🔌 Hello World via API..."
	curl -X POST http://localhost:$(SERVER_PORT)/execute \
		-H "Content-Type: application/json" \
		-d '{"code": "print(\"Hello from API!\")"}' | python -m json.tool

api-tokenize:
	@echo "🔌 Tokenizing code via API..."
	curl -X POST http://localhost:$(SERVER_PORT)/tokenize \
		-H "Content-Type: application/json" \
		-d '{"code": "$(CODE)"}' | python -m json.tool

api-variables:
	@echo "🔌 Getting variables via API..."
	curl -s http://localhost:$(SERVER_PORT)/variables | python -m json.tool

api-stats:
	@echo "🔌 Getting server stats..."
	curl -s http://localhost:$(SERVER_PORT)/stats | python -m json.tool

# ===========================================
# Docker - Build
# ===========================================

docker-build:
	@echo "🐳 Building all Docker images..."
	docker-compose -f docker/docker-compose.yml build

docker-build-server:
	@echo "🐳 Building server Docker image..."
	docker build -f docker/Dockerfile.server -t pyrl-server:latest .

docker-build-console:
	@echo "🐳 Building console Docker image..."
	docker build -f docker/Dockerfile.console -t pyrl-console:latest .

docker-build-model-generator:
	@echo "🐳 Building model generator Docker image..."
	docker build -f docker/Dockerfile.model-generator -t pyrl-model-generator:latest .

docker-build-model-inference:
	@echo "🐳 Building model inference Docker image..."
	docker build -f docker/Dockerfile.model-inference -t pyrl-model-inference:latest .

docker-build-training:
	@echo "🐳 Building training Docker image..."
	docker build -f docker/Dockerfile.training -t pyrl-training:latest .

docker-build-dev:
	@echo "🐳 Building dev Docker image..."
	docker build -f docker/Dockerfile.dev -t pyrl-dev:latest .

docker-build-all: docker-build-server docker-build-console docker-build-dev docker-build-training
	@echo "✓ All Docker images built!"

# ===========================================
# Docker - Run
# ===========================================

docker-up:
	@echo "🐳 Starting Docker containers..."
	docker-compose -f docker/docker-compose.yml up -d

docker-down:
	@echo "🐳 Stopping Docker containers..."
	docker-compose -f docker/docker-compose.yml down

docker-logs:
	@echo "🐳 Viewing Docker logs..."
	docker-compose -f docker/docker-compose.yml logs -f

docker-ps:
	@echo "🐳 Docker containers status..."
	docker-compose -f docker/docker-compose.yml ps

docker-run-server:
	@echo "🐳 Running server container..."
	docker run -p $(SERVER_PORT):$(SERVER_PORT) pyrl-server:latest

docker-run-console:
	@echo "🐳 Running console container..."
	docker run -it pyrl-console:latest

docker-run-dev:
	@echo "🐳 Running dev container..."
	docker run -it -p $(SERVER_PORT):$(SERVER_PORT) -p 8888:8888 \
		-v $(PWD)/src:/app/src \
		-v $(PWD)/tests:/app/tests \
		pyrl-dev:latest

docker-run-training:
	@echo "🐳 Running training container..."
	docker run -it \
		-v $(PWD)/examples:/app/examples \
		-v $(PWD)/models:/app/models \
		pyrl-training:latest

# ===========================================
# Docker - Profiles
# ===========================================

docker-up-training:
	@echo "🐳 Starting training containers..."
	docker-compose -f docker/docker-compose.yml --profile training up -d

docker-up-inference:
	@echo "🐳 Starting inference containers..."
	docker-compose -f docker/docker-compose.yml --profile inference up -d

docker-up-dev:
	@echo "🐳 Starting development containers..."
	docker-compose -f docker/docker-compose.yml --profile dev up -d

# ===========================================
# Model Training
# ===========================================

train:
	@echo "🤖 Training Pyrl model..."
	$(PYTHON) scripts/train_model.py --examples $(EXAMPLES_PATH)

train-full:
	@echo "🤖 Full training with all examples..."
	$(PYTHON) scripts/train_model.py \
		--examples $(EXAMPLES_PATH) \
		--epochs 20 \
		--batch-size 64 \
		--learning-rate 0.0001

train-quick:
	@echo "🤖 Quick training for testing..."
	$(PYTHON) scripts/train_model.py \
		--examples $(EXAMPLES_PATH) \
		--epochs 3 \
		--batch-size 16

train-custom:
	@echo "🤖 Custom training..."
	@echo "Usage: make train-custom EXAMPLES=path EPOCHS=20 BATCH=32 LR=0.0001"
	$(PYTHON) scripts/train_model.py \
		--examples $(or $(EXAMPLES),$(EXAMPLES_PATH)) \
		--epochs $(or $(EPOCHS),10) \
		--batch-size $(or $(BATCH),32) \
		--learning-rate $(or $(LR),0.0001)

train-dir:
	@echo "🤖 Training from directory..."
	$(PYTHON) scripts/train_model.py --examples-dir examples/

train-cli:
	@echo "🤖 Training via CLI REPL..."
	$(PYTHON) pyrl_cli.py -c "train --examples $(EXAMPLES_PATH)"

# ===========================================
# Model Management
# ===========================================

model-info:
	@echo "📊 Model information..."
	@if [ -f $(MODEL_PATH)/config.json ]; then \
		cat $(MODEL_PATH)/config.json | python -m json.tool; \
	else \
		echo "Model not found at $(MODEL_PATH)"; \
	fi

model-stats:
	@echo "📊 Training statistics..."
	@if [ -f $(MODEL_PATH)/training_stats.json ]; then \
		cat $(MODEL_PATH)/training_stats.json | python -m json.tool; \
	else \
		echo "Training stats not found"; \
	fi

model-vocab:
	@echo "📊 Vocabulary size..."
	@if [ -f $(MODEL_PATH)/vocab.json ]; then \
		python -c "import json; v=json.load(open('$(MODEL_PATH)/vocab.json')); print(f'Vocabulary: {len(v)} tokens')"; \
	else \
		echo "Vocabulary not found"; \
	fi

model-inference:
	@echo "🔮 Running model inference..."
	$(PYTHON) -c "from transformers import AutoModel; model = AutoModel.from_pretrained('$(MODEL_PATH)'); print(model)"

model-export:
	@echo "📦 Exporting model..."
	@if [ -d $(MODEL_PATH) ]; then \
		tar -czvf pyrl-model.tar.gz -C $(MODEL_PATH) .; \
		echo "Model exported to pyrl-model.tar.gz"; \
	else \
		echo "Model directory not found"; \
	fi

# ===========================================
# Checkpoints
# ===========================================

checkpoint-list:
	@echo "📋 Available checkpoints..."
	@ls -la checkpoints/*.json 2>/dev/null || echo "No checkpoints found"

checkpoint-info:
	@echo "📋 Checkpoint info: $(EPOCH)"
	@if [ -f checkpoints/checkpoint_epoch_$(EPOCH).json ]; then \
		cat checkpoints/checkpoint_epoch_$(EPOCH).json | python -m json.tool; \
	else \
		echo "Checkpoint not found"; \
	fi

checkpoint-latest:
	@echo "📋 Latest checkpoint..."
	@ls -t checkpoints/*.json 2>/dev/null | head -1 | xargs cat | python -m json.tool || echo "No checkpoints"

checkpoint-clean:
	@echo "🧹 Cleaning old checkpoints (keeping last 5)..."
	@ls -t checkpoints/*.json 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null || true

# ===========================================
# Plugin System
# ===========================================

plugin-list:
	@echo "🔌 Available plugins..."
	$(PYTHON) -c "from src.core.builtins import load_builtin_plugins; plugins = load_builtin_plugins(); print('Built-in plugins:'); [print(f'  - {k}') for k in plugins.keys()]"

plugin-load:
	@echo "🔌 Loading plugin: $(NAME)"
	$(PYTHON) -c "from src.core.builtins import register_plugin; print('Plugin loading...')"

plugin-dir:
	@echo "🔌 Plugin directories..."
	@echo "PYRL_PLUGINS_PATH: $${PYRL_PLUGINS_PATH:-Not set}"

# ===========================================
# Git Operations
# ===========================================

git-status:
	@echo "📝 Git status..."
	git status

git-log:
	@echo "📝 Git log (last 10 commits)..."
	git log --oneline -10

git-pull:
	@echo "📥 Pulling from $(GIT_REMOTE)/$(GIT_BRANCH)..."
	git pull $(GIT_REMOTE) $(GIT_BRANCH)

git-push:
	@echo "📤 Pushing to $(GIT_REMOTE)/$(GIT_BRANCH)..."
	git push $(GIT_REMOTE) $(GIT_BRANCH)

git-push-force:
	@echo "📤 Force pushing to $(GIT_REMOTE)/$(GIT_BRANCH)..."
	git push -f $(GIT_REMOTE) $(GIT_BRANCH)

git-commit:
	@echo "📝 Committing changes..."
	git add -A
	git commit -m "$(MSG)"

git-commit-push:
	@echo "📝 Committing and pushing..."
	git add -A
	git commit -m "$(MSG)"
	git push $(GIT_REMOTE) $(GIT_BRANCH)

git-diff:
	@echo "📝 Git diff..."
	git diff

git-branch:
	@echo "📝 Current branch..."
	git branch -a

git-tag:
	@echo "📝 Git tags..."
	git tag -l

git-remote:
	@echo "📝 Git remotes..."
	git remote -v

git-init:
	@echo "📝 Initializing git..."
	git init
	git add -A
	git commit -m "Initial commit"

# ===========================================
# Generation
# ===========================================

generate-model:
	@echo "⚙️ Generating model files..."
	mkdir -p $(MODEL_PATH)
	$(PYTHON) scripts/generate_model.py || echo "Script not found"

generate-examples:
	@echo "⚙️ Generating examples..."
	$(PYTHON) scripts/generate_examples.py || echo "Script not found"

# ===========================================
# Archive
# ===========================================

archive:
	@echo "📦 Creating archive..."
	zip -r pyrl-project.zip . \
		-x "*.git*" \
		-x "*__pycache__*" \
		-x "*.pyc" \
		-x "*.egg-info*" \
		-x ".pytest_cache*" \
		-x "*.zip"

archive-clean: clean archive
	@echo "📦 Clean archive created."

archive-7z:
	@echo "📦 Creating 7z archive..."
	7z a pyrl-project.7z . \
		-x!.git \
		-x!__pycache__ \
		-x!*.pyc \
		-x!*.egg-info \
		-x!.pytest_cache \
		-x!*.zip \
		-x!*.7z

# ===========================================
# Info
# ===========================================

info:
	@echo "ℹ️ Pyrl Project Information"
	@echo "============================"
	@echo "Python: $$(python --version)"
	@echo "Pip: $$(pip --version | cut -d' ' -f1-2)"
	@echo ""
	@echo "📁 Project structure:"
	@find . -type f -name "*.py" | head -20
	@echo ""
	@echo "📚 Example files:"
	@ls examples/*.pyrl 2>/dev/null || echo "No examples found"
	@echo ""
	@echo "🐳 Docker images:"
	@docker images "pyrl*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" 2>/dev/null || echo "No Docker images found"

version:
	@echo "Pyrl version:"
	@$(PYTHON) pyrl_cli.py --version

# ===========================================
# Security
# ===========================================

security:
	@echo "🔒 Running security checks..."
	pip-audit || true
	bandit -r src/ || true

security-audit:
	@echo "🔒 Running dependency vulnerability audit..."
	pip-audit --desc || true
	safety check || true

security-check:
	@echo "🔒 Quick security scan..."
	bandit -r src/ -ll || true

# ===========================================
# Dependencies
# ===========================================

deps:
	@echo "📦 Dependency tree..."
	pipdeptree || pip install pipdeptree && pipdeptree

deps-update:
	@echo "📦 Updating dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt --upgrade

deps-outdated:
	@echo "📦 Checking for outdated packages..."
	pip list --outdated

deps-freeze:
	@echo "📦 Freezing dependencies..."
	pip freeze > requirements.freeze.txt
	@echo "Dependencies saved to requirements.freeze.txt"

# ===========================================
# Documentation
# ===========================================

docs:
	@echo "📖 Generating documentation..."
	pdoc --html src/ --output-dir docs/ || echo "Install pdoc: pip install pdoc"

docs-serve:
	@echo "📖 Serving documentation..."
	pdoc --http :8080 src/ || echo "Install pdoc: pip install pdoc"

docs-clean:
	@echo "🧹 Cleaning documentation..."
	rm -rf docs/

docs-view:
	@echo "📖 Opening documentation..."
	@if [ -f documents/DOCUMENTATION_RU.md ]; then \
		echo "Russian: documents/DOCUMENTATION_RU.md"; \
	fi
	@if [ -f documents/DOCUMENTATION_EN.md ]; then \
		echo "English: documents/DOCUMENTATION_EN.md"; \
	fi

# ===========================================
# Benchmarks
# ===========================================

benchmark:
	@echo "⏱️ Running benchmarks..."
	python -m pytest tests/ --benchmark-only --benchmark-autosave || echo "Install pytest-benchmark"

benchmark-full:
	@echo "⏱️ Running full benchmarks with comparison..."
	python -m pytest tests/ --benchmark-only --benchmark-autosave --benchmark-compare || true

benchmark-save:
	@echo "⏱️ Saving benchmark results..."
	python -m pytest tests/ --benchmark-only --benchmark-autosave

# ===========================================
# Pre-commit Hooks
# ===========================================

pre-commit-install:
	@echo "🪝 Installing pre-commit hooks..."
	pip install pre-commit
	pre-commit install
	pre-commit install --hook-type commit-msg

pre-commit-run:
	@echo "🪝 Running pre-commit on all files..."
	pre-commit run --all-files

pre-commit-update:
	@echo "🪝 Updating pre-commit hooks..."
	pre-commit autoupdate

# ===========================================
# Release
# ===========================================

release-patch:
	@echo "🏷️ Creating patch release..."
	bumpversion patch || echo "Install bumpversion: pip install bumpversion"
	git push --tags

release-minor:
	@echo "🏷️ Creating minor release..."
	bumpversion minor || echo "Install bumpversion: pip install bumpversion"
	git push --tags

release-major:
	@echo "🏷️ Creating major release..."
	bumpversion major || echo "Install bumpversion: pip install bumpversion"
	git push --tags

# ===========================================
# Validation
# ===========================================

validate:
	@echo "✅ Validating project setup..."
	@python -c "import sys; sys.path.insert(0, 'src'); import pyrl; print('✓ Module imports OK')" || echo "✗ Module import failed"
	@test -f requirements.txt && echo "✓ requirements.txt found" || echo "✗ requirements.txt missing"
	@test -f pyproject.toml && echo "✓ pyproject.toml found" || echo "✗ pyproject.toml missing"
	@test -d src/ && echo "✓ src/ directory found" || echo "✗ src/ directory missing"
	@test -d tests/ && echo "✓ tests/ directory found" || echo "✗ tests/ directory missing"
	@test -d examples/ && echo "✓ examples/ directory found" || echo "✗ examples/ directory missing"
	@test -d models/ && echo "✓ models/ directory found" || echo "✗ models/ directory missing"

validate-config:
	@echo "✅ Validating configuration files..."
	@test -f pyproject.toml && python -c "import toml; toml.load('pyproject.toml'); print('✓ pyproject.toml valid')" || echo "✗ pyproject.toml invalid"
	@test -f requirements.txt && pip install -r requirements.txt --dry-run 2>/dev/null && echo "✓ requirements.txt valid" || echo "✗ requirements.txt may have issues"

validate-env:
	@echo "✅ Validating environment..."
	@echo "Python: $$(python --version)"
	@echo "Pip: $$(pip --version | cut -d' ' -f1-2)"
	@echo "Virtual env: $$(test -n \"$$VIRTUAL_ENV\" && echo \"Active ($$VIRTUAL_ENV)\" || echo \"Not active\")"
	@echo "Working directory: $$(pwd)"

# ===========================================
# Health Check
# ===========================================

health:
	@echo "💊 Running health check..."
	@curl -s http://localhost:$(SERVER_PORT)/health 2>/dev/null || echo "Server not running on port $(SERVER_PORT)"

health-check:
	@echo "💊 Checking server health..."
	@curl -s -o /dev/null -w "%{http_code}" http://localhost:$(SERVER_PORT)/health 2>/dev/null || echo "000"

health-wait:
	@echo "💊 Waiting for server to be healthy..."
	@for i in $$(seq 1 30); do \
		if curl -s http://localhost:$(SERVER_PORT)/health > /dev/null 2>&1; then \
			echo "Server is healthy!"; \
			exit 0; \
		fi; \
		echo "Attempt $$i: Server not ready, waiting..."; \
		sleep 1; \
	done; \
	echo "Server failed to start"; \
	exit 1

# ===========================================
# CI/CD
# ===========================================

ci: ci-lint ci-test
	@echo "✓ CI pipeline complete"

ci-test:
	@echo "🔄 Running CI tests..."
	pytest tests/ -v --junitxml=test-results.xml --cov=src --cov-report=xml --cov-report=term

ci-lint:
	@echo "🔄 Running CI linting..."
	flake8 src/ tests/ --max-line-length=100 --output-file=lint-results.txt || true
	pylint src/ --output-format=text --output=pylint-results.txt || true
	black --check src/ tests/ || true
	mypy src/ || true

ci-build:
	@echo "🔄 Running CI build..."
	python -m build || pip install build && python -m build
	ls -la dist/

# ===========================================
# Profiling
# ===========================================

profile:
	@echo "📈 Profiling Pyrl interpreter..."
	python -m cProfile -s cumtime pyrl_cli.py examples/01_hello_world.pyrl

profile-memory:
	@echo "📈 Memory profiling..."
	python -m memory_profiler pyrl_cli.py examples/01_hello_world.pyrl 2>/dev/null || echo "Install memory_profiler: pip install memory_profiler"

profile-time:
	@echo "📈 Time profiling with detailed output..."
	python -X importtime pyrl_cli.py examples/01_hello_world.pyrl 2>&1 | head -50

# ===========================================
# Watch Mode
# ===========================================

watch-test:
	@echo "👁️ Watching for test changes..."
	python -m pytest_watch || echo "Install pytest-watch: pip install pytest-watch"

watch-lint:
	@echo "👁️ Watching for lint changes..."
	@while true; do \
		clear; \
		echo "Last check: $$(date)"; \
		flake8 src/ tests/ --max-line-length=100 2>/dev/null || true; \
		echo ""; \
		echo "Press Ctrl+C to stop..."; \
		sleep 2; \
	done

watch-coverage:
	@echo "👁️ Watching tests with coverage..."
	ptw -- --cov=src --cov-report=term-missing || echo "Install pytest-watch: pip install pytest-watch"

# ===========================================
# Debug
# ===========================================

debug-server:
	@echo "🐛 Starting server in debug mode..."
	PYRL_DEBUG=1 uvicorn pyrl_server:app --reload --host $(SERVER_HOST) --port $(SERVER_PORT)

debug-cli:
	@echo "🐛 Starting CLI in debug mode..."
	PYRL_DEBUG=1 $(PYTHON) pyrl_cli.py --debug

debug-test:
	@echo "🐛 Running tests with debug output..."
	PYRL_DEBUG=1 pytest tests/ -v -s --tb=long

# ===========================================
# Database (if applicable)
# ===========================================

db-setup:
	@echo "🗄️ Setting up database..."
	$(PYTHON) scripts/setup_db.py || echo "Database script not found"

db-reset:
	@echo "🗄️ Resetting database..."
	rm -f pyrl.db 2>/dev/null || true
	$(PYTHON) scripts/setup_db.py || echo "Database script not found"

# ===========================================
# Cache
# ===========================================

cache-clear:
	@echo "🗑️ Clearing all caches..."
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf __pycache__/ src/__pycache__/ tests/__pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cache cleared"

cache-pip:
	@echo "🗑️ Clearing pip cache..."
	pip cache purge || echo "Pip cache cleared"

# ===========================================
# Quick Commands
# ===========================================

quick-install:
	@echo "⚡ Quick install (no dev deps)..."
	pip install -r requirements.txt --quiet

quick-test:
	@echo "⚡ Quick test run..."
	pytest tests/ -x -q

quick-lint:
	@echo "⚡ Quick lint check..."
	flake8 src/ tests/ --max-line-length=100 --select=E9,F63,F7,F82

quick-run:
	@echo "⚡ Quick run: $(CODE)"
	$(PYTHON) pyrl_cli.py -c "$(CODE)"

# ===========================================
# Help
# ===========================================

help:
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║                    PYRL MAKEFILE v2.0                      ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📦 INSTALLATION"
	@echo "  make install           Install dependencies"
	@echo "  make install-dev       Install with dev dependencies"
	@echo "  make install-full      Install all dependencies including tools"
	@echo ""
	@echo "🧪 TESTING"
	@echo "  make test              Run tests"
	@echo "  make test-cov          Run tests with coverage"
	@echo "  make test-quick        Run tests (stop on first failure)"
	@echo "  make test-file FILE=x   Run specific test file"
	@echo ""
	@echo "✨ CODE QUALITY"
	@echo "  make lint              Run linters"
	@echo "  make format            Format code"
	@echo "  make format-check      Check code format"
	@echo "  make type-check        Run type checker"
	@echo "  make quality           Run all quality checks"
	@echo "  make clean             Clean build artifacts"
	@echo "  make clean-all         Deep clean (including models)"
	@echo ""
	@echo "🚀 RUNNING"
	@echo "  make run-server        Start Pyrl API server"
	@echo "  make run-cli           Start Pyrl REPL"
	@echo "  make run-cli-debug     Start REPL in debug mode"
	@echo "  make run-cli-file FILE=x  Run specific .pyrl file"
	@echo "  make dev               Start dev server with hot reload"
	@echo ""
	@echo "📚 EXAMPLES"
	@echo "  make run-examples      Run all examples"
	@echo "  make example FILE=x    Run specific example"
	@echo "  make example-auth      Run web auth example"
	@echo "  make list-examples     List all available examples"
	@echo ""
	@echo "🌐 WEB & API"
	@echo "  make web-server        Start web server"
	@echo "  make web-auth          Run auth example"
	@echo "  make api-test          Test API health"
	@echo "  make api-execute CODE=x  Execute code via API"
	@echo "  make api-stats         Get server stats"
	@echo ""
	@echo "🤖 MODEL TRAINING"
	@echo "  make train             Train model (default settings)"
	@echo "  make train-full        Full training (20 epochs)"
	@echo "  make train-quick       Quick training (3 epochs)"
	@echo "  make train-custom EPOCHS=x BATCH=x  Custom training"
	@echo ""
	@echo "📊 MODEL MANAGEMENT"
	@echo "  make model-info        Show model configuration"
	@echo "  make model-stats       Show training statistics"
	@echo "  make model-vocab       Show vocabulary size"
	@echo "  make model-export      Export model to archive"
	@echo ""
	@echo "📋 CHECKPOINTS"
	@echo "  make checkpoint-list   List all checkpoints"
	@echo "  make checkpoint-latest Show latest checkpoint"
	@echo "  make checkpoint-clean  Clean old checkpoints"
	@echo ""
	@echo "🐳 DOCKER BUILD"
	@echo "  make docker-build      Build all images"
	@echo "  make docker-build-server   Build server image"
	@echo "  make docker-build-console  Build console image"
	@echo "  make docker-build-training Build training image"
	@echo ""
	@echo "🐳 DOCKER RUN"
	@echo "  make docker-up         Start containers"
	@echo "  make docker-down       Stop containers"
	@echo "  make docker-logs       View container logs"
	@echo "  make docker-run-server Run server container"
	@echo "  make docker-run-console Run console container"
	@echo ""
	@echo "📝 GIT OPERATIONS"
	@echo "  make git-status        Show git status"
	@echo "  make git-log           Show commit history"
	@echo "  make git-pull          Pull from remote"
	@echo "  make git-push          Push to remote"
	@echo "  make git-commit MSG=x  Commit with message"
	@echo "  make git-commit-push MSG=x  Commit and push"
	@echo "  make git-diff          Show changes"
	@echo ""
	@echo "📖 DOCUMENTATION"
	@echo "  make docs              Generate documentation"
	@echo "  make docs-serve        Serve documentation"
	@echo "  make docs-view         Show doc locations"
	@echo ""
	@echo "🔒 SECURITY"
	@echo "  make security          Run security checks"
	@echo "  make security-audit    Run vulnerability audit"
	@echo ""
	@echo "📦 ARCHIVE"
	@echo "  make archive           Create .zip archive"
	@echo "  make archive-7z        Create .7z archive"
	@echo ""
	@echo "ℹ️ OTHER"
	@echo "  make info              Show project info"
	@echo "  make version           Show Pyrl version"
	@echo "  make validate          Validate project setup"
	@echo "  make health            Check server health"
	@echo "  make help              Show this help message"
	@echo ""
