#!/usr/bin/env python3
"""MCP server for Japanese kanji conversion using kanjiconv."""

import asyncio
import logging
from typing import Any

from kanjiconv import KanjiConv
from kanjiconv.entities import SudachiDictType
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server instance
server = Server("kanjiconv-mcp")

# Initialize KanjiConv instances for different configurations
default_kanji_conv = KanjiConv(separator="/")
space_separated_kanji_conv = KanjiConv(separator=" ")
no_separator_kanji_conv = KanjiConv(separator="")


class ConvertRequest(BaseModel):
    """Request model for kanji conversion."""

    text: str
    separator: str = "/"
    use_custom_readings: bool = True
    use_unidic: bool = False
    sudachi_dict_type: str = "full"


def get_kanji_conv_instance(
    separator: str, use_custom_readings: bool, use_unidic: bool, sudachi_dict_type: str
) -> KanjiConv:
    """Get or create a KanjiConv instance with specified configuration."""
    dict_type = getattr(SudachiDictType, sudachi_dict_type.upper(), SudachiDictType.FULL).value
    return KanjiConv(
        separator=separator, use_custom_readings=use_custom_readings, use_unidic=use_unidic, sudachi_dict_type=dict_type
    )


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for kanji conversion."""
    return [
        Tool(
            name="convert_to_hiragana",
            description="Convert Japanese text (including kanji) to hiragana",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Japanese text to convert to hiragana"},
                    "separator": {
                        "type": "string",
                        "default": "/",
                        "description": "Separator character between words (default: '/', use '' for no separator)",
                    },
                    "use_custom_readings": {
                        "type": "boolean",
                        "default": True,
                        "description": "Use custom readings dictionary as fallback",
                    },
                    "use_unidic": {
                        "type": "boolean",
                        "default": False,
                        "description": "Use UniDic for improved reading accuracy",
                    },
                    "sudachi_dict_type": {
                        "type": "string",
                        "default": "full",
                        "enum": ["full", "small", "core"],
                        "description": "Type of Sudachi dictionary to use",
                    },
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="convert_to_katakana",
            description="Convert Japanese text (including kanji) to katakana",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Japanese text to convert to katakana"},
                    "separator": {
                        "type": "string",
                        "default": "/",
                        "description": "Separator character between words (default: '/', use '' for no separator)",
                    },
                    "use_custom_readings": {
                        "type": "boolean",
                        "default": True,
                        "description": "Use custom readings dictionary as fallback",
                    },
                    "use_unidic": {
                        "type": "boolean",
                        "default": False,
                        "description": "Use UniDic for improved reading accuracy",
                    },
                    "sudachi_dict_type": {
                        "type": "string",
                        "default": "full",
                        "enum": ["full", "small", "core"],
                        "description": "Type of Sudachi dictionary to use",
                    },
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="convert_to_roman",
            description="Convert Japanese text (including kanji) to roman alphabet",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Japanese text to convert to roman alphabet"},
                    "separator": {
                        "type": "string",
                        "default": "/",
                        "description": "Separator character between words (default: '/', use '' for no separator)",
                    },
                    "use_custom_readings": {
                        "type": "boolean",
                        "default": True,
                        "description": "Use custom readings dictionary as fallback",
                    },
                    "use_unidic": {
                        "type": "boolean",
                        "default": False,
                        "description": "Use UniDic for improved reading accuracy",
                    },
                    "sudachi_dict_type": {
                        "type": "string",
                        "default": "full",
                        "enum": ["full", "small", "core"],
                        "description": "Type of Sudachi dictionary to use",
                    },
                },
                "required": ["text"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls for kanji conversion."""
    try:
        if name == "convert_to_hiragana":
            request = ConvertRequest(**arguments)
            kanji_conv = get_kanji_conv_instance(
                request.separator, request.use_custom_readings, request.use_unidic, request.sudachi_dict_type
            )
            result = kanji_conv.to_hiragana(request.text)
            return [TextContent(type="text", text=result)]

        elif name == "convert_to_katakana":
            request = ConvertRequest(**arguments)
            kanji_conv = get_kanji_conv_instance(
                request.separator, request.use_custom_readings, request.use_unidic, request.sudachi_dict_type
            )
            result = kanji_conv.to_katakana(request.text)
            return [TextContent(type="text", text=result)]

        elif name == "convert_to_roman":
            request = ConvertRequest(**arguments)
            kanji_conv = get_kanji_conv_instance(
                request.separator, request.use_custom_readings, request.use_unidic, request.sudachi_dict_type
            )
            result = kanji_conv.to_roman(request.text)
            return [TextContent(type="text", text=result)]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting kanjiconv MCP server...")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="kanjiconv-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(), experimental_capabilities={}
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
