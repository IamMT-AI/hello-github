.PHONY: help setup install format lint test clean run-api run-stylize run-fusion docker-build

# Default target
help:
	@echo "Available targets:"
	@echo "  setup       - Set up development environment"
	@echo "  install     - Install dependencies"
	@echo "  format      - Format code with black and isort"
	@echo "  lint        - Run linting with flake8 and mypy"
	@echo "  test        - Run tests"
	@echo "  clean       - Clean up temporary files"
	@echo "  run-api     - Run API gateway server"
	@echo "  run-stylize - Run 2D stylization service"
	@echo "  run-fusion  - Run fusion service"
	@echo "  docker-build - Build Docker base image"

# Development environment setup
setup: install
	@echo "Development environment ready!"

install:
	pip install -r requirements.txt

# Code formatting and linting
format:
	black .
	isort .

lint:
	flake8 .
	mypy apps/ services/ libs/ --ignore-missing-imports

# Testing
test:
	pytest -v

# Cleanup
clean:
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

# Services
run-api:
	cd apps/api-gateway && uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-stylize:
	cd services/stylize2d && uvicorn server:app --reload --host 0.0.0.0 --port 8001

run-fusion:
	cd services/fusion && python -c "from fuse import fuse_face_body; print('Fusion service ready - use as library')"

# Docker
docker-build:
	docker build -f docker/Dockerfile.base -t hello-github-mvp:base .