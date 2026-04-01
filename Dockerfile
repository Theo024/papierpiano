# Multi-stage Dockerfile for Sanic API with Vite React frontend

# Stage 1: Build the React frontend
FROM node:24-slim@sha256:06e5c9f86bfa0aaa7163cf37a5eaa8805f16b9acb48e3f85645b09d459fc2a9f AS frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build the frontend
RUN npm run build

# Stage 2: Build the Python API
FROM python:3.14-slim@sha256:fb83750094b46fd6b8adaa80f66e2302ecbe45d513f6cece637a841e1025b4ca AS backend-builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest@sha256:90bbb3c16635e9627f49eec6539f956d70746c409209041800a0280b93152823 /uv /uvx /usr/local/bin/

# Set working directory
WORKDIR /app

# Copy Python dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --locked --no-install-project --no-editable

# Copy the project into the intermediate image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

# Stage 3: Production runtime
FROM python:3.14-slim@sha256:fb83750094b46fd6b8adaa80f66e2302ecbe45d513f6cece637a841e1025b4ca AS runtime

# Create non-root user
RUN groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=backend-builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy built frontend from frontend-builder
COPY --from=frontend-builder --chown=appuser:appuser /app/frontend/dist ./static

COPY --chown=appuser:appuser assets ./assets

# Ensure the virtual environment is in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["sanic", "papierpiano:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
