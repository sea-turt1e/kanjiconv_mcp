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

1. Clone this repository:
```bash
git clone <repository-url>
cd kanjiconv_mcp
```

2. Install dependencies:
```bash
uv sync
```

## Usage

### With Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "kanjiconv": {
      "command": "uv",
      "args": ["run", "python", "/path/to/kanjiconv_mcp/main.py"],
      "cwd": "/path/to/kanjiconv_mcp"
    }
  }
}
```

### Manual Usage

Run the server directly:
```bash
uv run python main.py
```

## Example Usage

- Convert "漢字をひらがなに変換します" to hiragana → "かんじ/を/ひらがな/に/へんかん/し/ます"
- Convert "こんにちは世界" to katakana → "コンニチハ/セカイ"  
- Convert "日本語" to roman → "nihongo"

## License

Apache License 2.0
