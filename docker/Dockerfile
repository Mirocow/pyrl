# ============================================================================
# Pyrl Ecosystem Dockerfile
# Multi-stage build for optimized production image
# ============================================================================

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ============================================================================
# Stage 2: Production
# ============================================================================
FROM python:3.11-slim as production

LABEL maintainer="Pyrl Ecosystem Team"
LABEL version="2.0.0"
LABEL description="Pyrl Virtual Machine with AI Assistant and Plugin System"

WORKDIR /app

# Create non-root user for security
RUN groupadd -r pyrl && useradd -r -g pyrl pyrl

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy source files
COPY --chown=pyrl:pyrl src/ ./src/
COPY --chown=pyrl:pyrl plugins/ ./plugins/
COPY --chown=pyrl:pyrl training/ ./training/
COPY --chown=pyrl:pyrl examples/ ./examples/

# Create directories
RUN mkdir -p /app/models /app/output /app/logs && \
    chown -R pyrl:pyrl /app

# Switch to non-root user
USER pyrl

# Set environment variables
ENV PYRL_PLUGINS_DIR=/app/plugins
ENV PYRL_OUTPUT_DIR=/app/output
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "-m", "src.pyrl_vm"]

# ============================================================================
# Stage 3: Development
# ============================================================================
FROM production as development

USER root

# Install development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Install additional dev dependencies
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    black \
    flake8 \
    mypy \
    jupyter

USER pyrl

# Development command with interactive shell
CMD ["/bin/bash"]

# ============================================================================
# Stage 4: Training (GPU-enabled)
# ============================================================================
FROM nvidia/cuda:11.8-devel-ubuntu22.04 as training

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-venv \
    python3-pip \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

WORKDIR /training

# Copy training files
COPY training/ .
COPY src/ ../app/src/

# Install ML dependencies
RUN pip install --no-cache-dir \
    torch \
    transformers \
    datasets \
    accelerate \
    peft \
    bitsandbytes \
    trl \
    lark \
    tensorboard

# Create output directory
RUN mkdir -p /models

# Training entrypoint
CMD ["python", "train_model.py"]

# ============================================================================
# Stage 5: API Server
# ============================================================================
FROM production as api

# Install additional dependencies for API
USER root
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pydantic
USER pyrl

# Copy API server code
COPY --chown=pyrl:pyrl docker/api_server.py .

# Expose port
EXPOSE 8000

# Run API server
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
