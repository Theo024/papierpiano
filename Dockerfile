# Multi-stage Dockerfile for Sanic API with Vite React frontend

# Stage 1: Build the React frontend
FROM node:22-slim@sha256:06c48f4e9fccaf313465eb533d3f57bb25e2de29ffbc86ed821ef1da92f1368c AS frontend-builder

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
FROM python:3.13-slim@sha256:6f79e7a10bb7d0b0a50534a70ebc78823f941fba26143ecd7e6c5dca9d7d7e8a AS backend-builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest@sha256:cda9608307dbbfc1769f3b6b1f9abf5f1360de0be720f544d29a7ae2863c47ef /uv /uvx /usr/local/bin/

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
FROM python:3.13-slim@sha256:6f79e7a10bb7d0b0a50534a70ebc78823f941fba26143ecd7e6c5dca9d7d7e8a AS runtime

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
