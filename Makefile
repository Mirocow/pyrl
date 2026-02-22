# Pyrl Makefile
# Build and development commands for Pyrl language platform

.PHONY: all install test lint clean run help docker-build docker-up docker-down \
        security security-audit security-check deps deps-update deps-outdated \
        docs docs-serve docs-clean benchmark benchmark-full \
        pre-commit pre-commit-install pre-commit-run \
        release release-patch release-minor release-major \
        validate validate-config validate-env \
        health health-check \
        ci ci-test ci-lint ci-build \
        profile profile-memory profile-time \
        watch watch-test watch-lint

# ===========================================
# Default
# ===========================================

all: install

# ===========================================
# Installation
# ===========================================

install:
        @echo "Installing dependencies..."
        pip install -r requirements.txt

install-dev:
        @echo "Installing development dependencies..."
        pip install -r requirements.txt
        pip install -e .

# ===========================================
# Testing
# ===========================================

test:
        @echo "Running tests..."
        pytest tests/ -v --tb=short

test-cov:
        @echo "Running tests with coverage..."
        pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-quick:
        @echo "Running quick tests..."
        pytest tests/ -v -x --tb=line

# ===========================================
# Code Quality
# ===========================================

lint:
        @echo "Running linter..."
        flake8 src/ tests/ --max-line-length=100 || true
        pylint src/ || true

format:
        @echo "Formatting code..."
        black src/ tests/
        isort src/ tests/

format-check:
        @echo "Checking code format..."
        black --check src/ tests/
        isort --check src/ tests/

type-check:
        @echo "Running type checker..."
        mypy src/ || true

# ===========================================
# Cleaning
# ===========================================

clean:
        @echo "Cleaning build artifacts..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete
        rm -rf .pytest_cache/ .coverage htmlcov/ .tox/ dist/ build/

# ===========================================
# Running
# ===========================================

run-server:
        @echo "Starting Pyrl server..."
        python pyrl_server.py

run-cli:
        @echo "Starting Pyrl CLI..."
        python pyrl_cli.py

run-cli-debug:
        @echo "Starting Pyrl CLI in debug mode..."
        python pyrl_cli.py --debug

dev:
        @echo "Starting development server..."
        uvicorn pyrl_server:app --reload --host 0.0.0.0 --port 8000

# ===========================================
# Examples
# ===========================================

run-examples:
        @echo "Running all examples..."
        for f in examples/*.pyrl; do \
                echo "\n=== Running $$f ==="; \
                python pyrl_cli.py "$$f" || true; \
        done

example:
        @echo "Run specific example: make example FILE=01_hello_world"
        python pyrl_cli.py examples/$(FILE).pyrl

# ===========================================
# Docker - Build
# ===========================================

docker-build:
        @echo "Building all Docker images..."
        docker-compose -f docker/docker-compose.yml build

docker-build-server:
        @echo "Building server Docker image..."
        docker build -f docker/Dockerfile.server -t pyrl-server:latest .

docker-build-console:
        @echo "Building console Docker image..."
        docker build -f docker/Dockerfile.console -t pyrl-console:latest .

docker-build-model-generator:
        @echo "Building model generator Docker image..."
        docker build -f docker/Dockerfile.model-generator -t pyrl-model-generator:latest .

docker-build-model-inference:
        @echo "Building model inference Docker image..."
        docker build -f docker/Dockerfile.model-inference -t pyrl-model-inference:latest .

docker-build-training:
        @echo "Building training Docker image..."
        docker build -f docker/Dockerfile.training -t pyrl-training:latest .

docker-build-dev:
        @echo "Building dev Docker image..."
        docker build -f docker/Dockerfile.dev -t pyrl-dev:latest .

# ===========================================
# Docker - Run
# ===========================================

docker-up:
        @echo "Starting Docker containers..."
        docker-compose -f docker/docker-compose.yml up -d

docker-down:
        @echo "Stopping Docker containers..."
        docker-compose -f docker/docker-compose.yml down

docker-logs:
        docker-compose -f docker/docker-compose.yml logs -f

docker-ps:
        docker-compose -f docker/docker-compose.yml ps

docker-run-server:
        docker run -p 8000:8000 pyrl-server:latest

docker-run-console:
        docker run -it pyrl-console:latest

docker-run-dev:
        docker run -it -p 8000:8000 -p 8888:8888 \
                -v $(PWD)/src:/app/src \
                -v $(PWD)/tests:/app/tests \
                pyrl-dev:latest

# ===========================================
# Docker - Profiles
# ===========================================

docker-up-training:
        @echo "Starting training containers..."
        docker-compose -f docker/docker-compose.yml --profile training up -d

docker-up-inference:
        @echo "Starting inference containers..."
        docker-compose -f docker/docker-compose.yml --profile inference up -d

docker-up-dev:
        @echo "Starting development containers..."
        docker-compose -f docker/docker-compose.yml --profile dev up -d

# ===========================================
# Generation
# ===========================================

generate-model:
        @echo "Generating model files..."
        mkdir -p models/pyrl-model
        python scripts/generate_model.py || echo "Script not found"

generate-examples:
        @echo "Generating examples..."
        python scripts/generate_examples.py || echo "Script not found"

# ===========================================
# Training
# ===========================================

train:
        @echo "Training Pyrl model..."
        python scripts/train_model.py --examples examples/10000_examples.pyrl

train-custom:
        @echo "Train with custom options..."
        @echo "Usage: make train-custom EXAMPLES=path/to/examples.pyrl EPOCHS=20"
        python scripts/train_model.py --examples $(or $(EXAMPLES),examples/10000_examples.pyrl) --epochs $(or $(EPOCHS),10)

train-full:
        @echo "Full training with all examples..."
        python scripts/train_model.py --examples examples/10000_examples.pyrl --epochs 20 --batch-size 64

train-quick:
        @echo "Quick training for testing..."
        python scripts/train_model.py --examples examples/10000_examples.pyrl --epochs 3 --batch-size 16

train-dir:
        @echo "Training from directory..."
        python scripts/train_model.py --examples-dir examples/

# ===========================================
# Archive
# ===========================================

archive:
        @echo "Creating archive..."
        zip -r pyrl-project.zip . \
                -x "*.git*" \
                -x "*__pycache__*" \
                -x "*.pyc" \
                -x "*.egg-info*" \
                -x ".pytest_cache*" \
                -x "*.zip"

archive-clean: clean archive
        @echo "Clean archive created."

# ===========================================
# Info
# ===========================================

info:
        @echo "Pyrl Project Information"
        @echo "========================"
        @echo "Python version: $$(python --version)"
        @echo "Pip version: $$(pip --version)"
        @echo ""
        @echo "Project structure:"
        @find . -type f -name "*.py" | head -20
        @echo ""
        @echo "Example files:"
        @ls examples/*.pyrl 2>/dev/null || echo "No examples found"
        @echo ""
        @echo "Docker images:"
        @docker images "pyrl*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" 2>/dev/null || echo "No Docker images found"

# ===========================================
# Security
# ===========================================

security:
        @echo "Running security checks..."
        pip-audit || true
        bandit -r src/ || true

security-audit:
        @echo "Running dependency vulnerability audit..."
        pip-audit --desc || true
        safety check || true

security-check:
        @echo "Quick security scan..."
        bandit -r src/ -ll || true

# ===========================================
# Dependencies
# ===========================================

deps:
        @echo "Showing dependency tree..."
        pipdeptree || pip install pipdeptree && pipdeptree

deps-update:
        @echo "Updating dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt --upgrade

deps-outdated:
        @echo "Checking for outdated packages..."
        pip list --outdated

deps-freeze:
        @echo "Freezing dependencies..."
        pip freeze > requirements.freeze.txt
        @echo "Dependencies saved to requirements.freeze.txt"

# ===========================================
# Documentation
# ===========================================

docs:
        @echo "Generating documentation..."
        pdoc --html src/ --output-dir docs/ || echo "Install pdoc: pip install pdoc"

docs-serve:
        @echo "Serving documentation..."
        pdoc --http :8080 src/ || echo "Install pdoc: pip install pdoc"

docs-clean:
        @echo "Cleaning documentation..."
        rm -rf docs/

# ===========================================
# Benchmarks
# ===========================================

benchmark:
        @echo "Running benchmarks..."
        python -m pytest tests/ --benchmark-only --benchmark-autosave || echo "Install pytest-benchmark"

benchmark-full:
        @echo "Running full benchmarks with comparison..."
        python -m pytest tests/ --benchmark-only --benchmark-autosave --benchmark-compare || true

benchmark-save:
        @echo "Saving benchmark results..."
        python -m pytest tests/ --benchmark-only --benchmark-autosave

# ===========================================
# Pre-commit Hooks
# ===========================================

pre-commit-install:
        @echo "Installing pre-commit hooks..."
        pip install pre-commit
        pre-commit install
        pre-commit install --hook-type commit-msg

pre-commit-run:
        @echo "Running pre-commit on all files..."
        pre-commit run --all-files

pre-commit-update:
        @echo "Updating pre-commit hooks..."
        pre-commit autoupdate

# ===========================================
# Release
# ===========================================

release-patch:
        @echo "Creating patch release..."
        @python -c "import toml; d=toml.load('pyproject.toml'); v=d['project']['version'].split('.'); v[2]=str(int(v[2])+1); print('.'.join(v))" 2>/dev/null || echo "Version bump manually"
        git tag -a "v$$(python -c 'import toml; print(toml.load(\"pyproject.toml\")[\"project\"][\"version\"])')" -m "Patch release" 2>/dev/null || echo "Create tag manually"

release-minor:
        @echo "Creating minor release..."
        @python -c "import toml; d=toml.load('pyproject.toml'); v=d['project']['version'].split('.'); v[1]=str(int(v[1])+1); v[2]='0'; print('.'.join(v))" 2>/dev/null || echo "Version bump manually"

release-major:
        @echo "Creating major release..."
        @python -c "import toml; d=toml.load('pyproject.toml'); v=d['project']['version'].split('.'); v[0]=str(int(v[0])+1); v[1]='0'; v[2]='0'; print('.'.join(v))" 2>/dev/null || echo "Version bump manually"

# ===========================================
# Validation
# ===========================================

validate:
        @echo "Validating project setup..."
        @python -c "import sys; sys.path.insert(0, 'src'); import pyrl; print('✓ Module imports OK')" || echo "✗ Module import failed"
        @test -f requirements.txt && echo "✓ requirements.txt found" || echo "✗ requirements.txt missing"
        @test -f pyproject.toml && echo "✓ pyproject.toml found" || echo "✗ pyproject.toml missing"
        @test -d src/ && echo "✓ src/ directory found" || echo "✗ src/ directory missing"
        @test -d tests/ && echo "✓ tests/ directory found" || echo "✗ tests/ directory missing"
        @test -d examples/ && echo "✓ examples/ directory found" || echo "✗ examples/ directory missing"

validate-config:
        @echo "Validating configuration files..."
        @test -f pyproject.toml && python -c "import toml; toml.load('pyproject.toml'); print('✓ pyproject.toml valid')" || echo "✗ pyproject.toml invalid"
        @test -f requirements.txt && pip install -r requirements.txt --dry-run 2>/dev/null && echo "✓ requirements.txt valid" || echo "✗ requirements.txt may have issues"

validate-env:
        @echo "Validating environment..."
        @echo "Python: $$(python --version)"
        @echo "Pip: $$(pip --version | cut -d' ' -f1-2)"
        @echo "Virtual env: $$(test -n \"$$VIRTUAL_ENV\" && echo \"Active ($$VIRTUAL_ENV)\" || echo \"Not active\")"
        @echo "Working directory: $$(pwd)"

# ===========================================
# Health Check
# ===========================================

health:
        @echo "Running health check..."
        @curl -s http://localhost:8000/health 2>/dev/null || echo "Server not running on port 8000"

health-check:
        @echo "Checking server health..."
        @curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "000"

health-wait:
        @echo "Waiting for server to be healthy..."
        @for i in $$(seq 1 30); do \
                if curl -s http://localhost:8000/health > /dev/null 2>&1; then \
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
        @echo "CI pipeline complete"

ci-test:
        @echo "Running CI tests..."
        pytest tests/ -v --junitxml=test-results.xml --cov=src --cov-report=xml --cov-report=term

ci-lint:
        @echo "Running CI linting..."
        flake8 src/ tests/ --max-line-length=100 --output-file=lint-results.txt || true
        pylint src/ --output-format=text --output=pylint-results.txt || true
        black --check src/ tests/ || true
        mypy src/ || true

ci-build:
        @echo "Running CI build..."
        python -m build || pip install build && python -m build
        ls -la dist/

# ===========================================
# Profiling
# ===========================================

profile:
        @echo "Profiling Pyrl interpreter..."
        python -m cProfile -s cumtime pyrl_cli.py examples/01_hello_world.pyrl

profile-memory:
        @echo "Memory profiling..."
        python -m memory_profiler pyrl_cli.py examples/01_hello_world.pyrl 2>/dev/null || echo "Install memory_profiler: pip install memory_profiler"

profile-time:
        @echo "Time profiling with detailed output..."
        python -X importtime pyrl_cli.py examples/01_hello_world.pyrl 2>&1 | head -50

# ===========================================
# Watch Mode
# ===========================================

watch-test:
        @echo "Watching for test changes..."
        python -m pytest_watch || echo "Install pytest-watch: pip install pytest-watch"

watch-lint:
        @echo "Watching for lint changes..."
        @while true; do \
                clear; \
                echo "Last check: $$(date)"; \
                flake8 src/ tests/ --max-line-length=100 2>/dev/null || true; \
                echo ""; \
                echo "Press Ctrl+C to stop..."; \
                sleep 2; \
        done

watch-coverage:
        @echo "Watching tests with coverage..."
        ptw -- --cov=src --cov-report=term-missing || echo "Install pytest-watch: pip install pytest-watch"

# ===========================================
# Debug
# ===========================================

debug-server:
        @echo "Starting server in debug mode..."
        PYRL_DEBUG=1 uvicorn pyrl_server:app --reload --host 0.0.0.0 --port 8000

debug-cli:
        @echo "Starting CLI in debug mode..."
        PYRL_DEBUG=1 python pyrl_cli.py --debug

debug-test:
        @echo "Running tests with debug output..."
        PYRL_DEBUG=1 pytest tests/ -v -s --tb=long

# ===========================================
# Database (if applicable)
# ===========================================

db-setup:
        @echo "Setting up database..."
        python scripts/setup_db.py || echo "Database script not found"

db-reset:
        @echo "Resetting database..."
        rm -f pyrl.db 2>/dev/null || true
        python scripts/setup_db.py || echo "Database script not found"

# ===========================================
# Cache
# ===========================================

cache-clear:
        @echo "Clearing all caches..."
        rm -rf .pytest_cache/
        rm -rf .mypy_cache/
        rm -rf __pycache__/ src/__pycache__/ tests/__pycache__/
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        @echo "Cache cleared"

cache-pip:
        @echo "Clearing pip cache..."
        pip cache purge || echo "Pip cache cleared"

# ===========================================
# Quick Commands
# ===========================================

quick-install:
        @echo "Quick install (no dev deps)..."
        pip install -r requirements.txt --quiet

quick-test:
        @echo "Quick test run..."
        pytest tests/ -x -q

quick-lint:
        @echo "Quick lint check..."
        flake8 src/ tests/ --max-line-length=100 --select=E9,F63,F7,F82

# ===========================================
# Help
# ===========================================

help:
        @echo "Pyrl Makefile Commands"
        @echo "======================"
        @echo ""
        @echo "Installation:"
        @echo "  make install          - Install dependencies"
        @echo "  make install-dev      - Install with dev dependencies"
        @echo ""
        @echo "Testing:"
        @echo "  make test             - Run tests"
        @echo "  make test-cov         - Run tests with coverage"
        @echo "  make test-quick       - Run tests (stop on first failure)"
        @echo ""
        @echo "Code Quality:"
        @echo "  make lint             - Run linters"
        @echo "  make format           - Format code"
        @echo "  make format-check     - Check code format"
        @echo "  make type-check       - Run type checker"
        @echo "  make clean            - Clean build artifacts"
        @echo ""
        @echo "Running:"
        @echo "  make run-server       - Start Pyrl server"
        @echo "  make run-cli          - Start Pyrl REPL"
        @echo "  make run-cli-debug    - Start Pyrl REPL (debug mode)"
        @echo "  make dev              - Start dev server with reload"
        @echo ""
        @echo "Examples:"
        @echo "  make run-examples     - Run all examples"
        @echo "  make example FILE=01  - Run specific example"
        @echo ""
        @echo "Docker Build:"
        @echo "  make docker-build              - Build all images"
        @echo "  make docker-build-server       - Build server image"
        @echo "  make docker-build-console      - Build console image"
        @echo "  make docker-build-dev          - Build dev image"
        @echo "  make docker-build-training     - Build training image"
        @echo ""
        @echo "Docker Run:"
        @echo "  make docker-up                 - Start containers"
        @echo "  make docker-down               - Stop containers"
        @echo "  make docker-logs               - View logs"
        @echo "  make docker-run-server         - Run server container"
        @echo "  make docker-run-console        - Run console container"
        @echo "  make docker-run-dev            - Run dev container"
        @echo ""
        @echo "Docker Profiles:"
        @echo "  make docker-up-training        - Start training profile"
        @echo "  make docker-up-inference       - Start inference profile"
        @echo "  make docker-up-dev             - Start dev profile"
        @echo ""
        @echo "Other:"
        @echo "  make archive          - Create project archive"
        @echo "  make info             - Show project info"
        @echo "  make help             - Show this help"
