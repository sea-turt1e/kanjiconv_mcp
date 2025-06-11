# kanjiconv MCP Server

Japanese kanji conversion MCP server using [kanjiconv](https://github.com/sea-turt1e/kanjiconv) library.

## Features

This MCP server provides Japanese text conversion tools:

- **convert_to_hiragana**: Convert Japanese text (including kanji) to hiragana
- **convert_to_katakana**: Convert Japanese text (including kanji) to katakana  
- **convert_to_roman**: Convert Japanese text (including kanji) to roman alphabet

All tools support various options including:
- Custom separator characters between words
- Use of custom readings dictionary
- UniDic integration for improved accuracy
- Different Sudachi dictionary types (full, small, core)

## Installation

### Option 1: Using uv (Recommended)

1. Clone this repository:
```bash
git clone kanjiconv_mcp
cd kanjiconv_mcp
```

2. Install dependencies:
```bash
uv sync
```

### Option 2: Using pip

1. Clone this repository:
```bash
git clone kanjiconv_mcp
cd kanjiconv_mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
python -m unidic download
```

### Option 3: Using Docker
Build and run with Docker:
```bash
# Build using uv (default)
docker build -t kanjiconv-mcp .

# Or build using pip
docker build -f Dockerfile.pip -t kanjiconv-mcp .

# Run the container
docker run -p 8000:8000 kanjiconv-mcp
```

Or use the provided helper script:
```bash
# Make the script executable
chmod +x docker.sh

# Build and run
./docker.sh build
./docker.sh up
```

## Usage

### With Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

#### For local installation:
```json
{
  "mcpServers": {
    "kanjiconv": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/kanjiconv_mcp",
        "run",
        "python",
        "main.py"
      ]
        }
    }
}
```

#### For Docker installation:
```json
{
  "mcpServers": {
    "kanjiconv": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "kanjiconv-mcp:latest"],
      "cwd": "/path/to/kanjiconv_mcp"
    }
  }
}
```

### Manual Usage

#### Local installation:
```bash
# With uv
uv run python main.py

# With pip
python main.py
```

#### Docker:
```bash
# Using docker command directly
docker run --rm -it kanjiconv-mcp

# Using helper script
./docker.sh test
```

### Docker Helper Script

The `docker.sh` script provides convenient commands for Docker operations:

```bash
# Build Docker image (tries uv first, falls back to pip)
./docker.sh build

# Build explicitly with pip
./docker.sh build-pip

# Start server with docker-compose
./docker.sh up

# Stop server
./docker.sh down

# View logs
./docker.sh logs

# Restart server
./docker.sh restart

# Run in test mode (interactive)
./docker.sh test

# Open shell in container
./docker.sh shell

# Clean up Docker resources
./docker.sh clean

# Show help
./docker.sh help
```

## Example Usage

- Convert "漢字をひらがなに変換します" to hiragana → "かんじ/を/ひらがな/に/へんかん/し/ます"
- Convert "こんにちは世界" to katakana → "コンニチハ/セカイ"  
- Convert "日本語" to roman → "nihongo"

## Docker Files

This project includes multiple Docker configurations:

### Dockerfile (Default)
- Uses `uv` for fast dependency management
- Multi-stage build for optimized image size
- Includes Rust compiler for building `sudachipy`
- Recommended for modern Python workflows

### Dockerfile.pip
- Uses traditional `pip` for dependency management
- Compatible with environments that don't support `uv`
- Single-stage build for simplicity
- Fallback option when `uv` is not available

### docker.sh
- Convenient shell script for Docker operations
- Automatically tries `uv` first, falls back to `pip`
- Includes commands for building, running, logging, and cleanup
- Supports both standalone Docker and docker-compose workflows

### docker-compose.yml
- Orchestrates the kanjiconv MCP server
- Maps stdio for MCP communication
- Configures proper environment variables
- Enables easy service management

## License

Apache License 2.0
