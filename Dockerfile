# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv using pip (simpler and more reliable)
RUN pip install uv

# Set environment variables for uv
ENV UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1

# Copy project configuration files
COPY pyproject.toml ./

# Install dependencies using uv
RUN uv sync --no-dev

# Copy application code
COPY main.py ./

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run the MCP server
CMD ["uv", "run", "python", "main.py"]
