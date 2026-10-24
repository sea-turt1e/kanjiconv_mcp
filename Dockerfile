# Use Python 3.15.1-slim-bookworm as the base image (patched for the eMudhra CA compromise)
FROM python:3.15.1-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /uvx /bin/

# Update ca-certificates (eMudhra CA fix) and install system dependencies including Rust compiler
RUN apt-get update && apt-get install -y --only-upgrade ca-certificates \
    && apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Rust compiler for building sudachipy
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && . /root/.cargo/env
ENV PATH="/root/.cargo/bin:$PATH"

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

# Install additional dependencies
RUN uv run python -m unidic download

# Copy application code
COPY main.py ./

# Expose port (if needed for future extensions)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run the MCP server
CMD ["uv", "run", "python", "main.py"]
