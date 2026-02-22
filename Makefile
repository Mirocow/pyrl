# Pyrl Makefile

.PHONY: help install test lint format clean docker-build docker-run

help:
	@echo "Pyrl Commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run all tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make lint         - Run linting"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make train        - Train the AI model"

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/

clean:
	rm -rf __pycache__ .pytest_cache htmlcov .coverage
	rm -rf src/__pycache__ tests/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -f docker/Dockerfile --target production -t pyrl:latest .

docker-run:
	docker run -it --rm pyrl:latest

docker-dev:
	docker build -f docker/Dockerfile --target development -t pyrl:dev .
	docker run -it --rm -v $(PWD)/src:/app/src -v $(PWD)/tests:/app/tests pyrl:dev

docker-api:
	docker build -f docker/Dockerfile --target api -t pyrl:api .
	docker run -it --rm -p 8000:8000 pyrl:api

train:
	python training/train_model.py --config training/train_config.yaml

train-test:
	python training/train_model.py --config training/train_config.yaml --test
