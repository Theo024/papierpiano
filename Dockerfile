# Multi-stage Dockerfile for Sanic API with Vite React frontend

# Stage 1: Build the React frontend
FROM node:22-slim@sha256:f9f7f95dcf1f007b007c4dcd44ea8f7773f931b71dc79d57c216e731c87a090b AS frontend-builder

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
FROM python:3.14-slim@sha256:5cfac249393fa6c7ebacaf0027a1e127026745e603908b226baa784c52b9d99b AS backend-builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest@sha256:f459f6f73a8c4ef5d69f4e6fbbdb8af751d6fa40ec34b39a1ab469acd6e289b7 /uv /uvx /usr/local/bin/

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
FROM python:3.14-slim@sha256:5cfac249393fa6c7ebacaf0027a1e127026745e603908b226baa784c52b9d99b AS runtime

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
