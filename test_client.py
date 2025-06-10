#!/usr/bin/env python3
"""Test client for kanjiconv MCP server."""

import asyncio
import json
import sys
from typing import Any, Dict


async def test_mcp_server():
    """Test the kanjiconv MCP server."""
    print("Testing kanjiconv MCP server...")

    # Start the MCP server process
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "main.py",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    async def send_request(request: Dict[str, Any]) -> Dict[str, Any]:
        """Send a request to the MCP server."""
        request_str = json.dumps(request) + "\n"
        process.stdin.write(request_str.encode())
        await process.stdin.drain()

        response_line = await process.stdout.readline()
        return json.loads(response_line.decode())

    try:
        # Initialize the server
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"},
            },
        }

        print("Sending initialize request...")
        init_response = await send_request(init_request)
        print(f"Initialize response: {init_response}")

        # List tools
        list_tools_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}

        print("\nListing tools...")
        tools_response = await send_request(list_tools_request)
        print(f"Tools response: {tools_response}")

        # Test hiragana conversion
        hiragana_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "convert_to_hiragana", "arguments": {"text": "こんにちは、世界！"}},
        }

        print("\nTesting hiragana conversion...")
        hiragana_response = await send_request(hiragana_request)
        print(f"Hiragana response: {hiragana_response}")

        # Test katakana conversion
        katakana_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "convert_to_katakana", "arguments": {"text": "こんにちは、世界！"}},
        }

        print("\nTesting katakana conversion...")
        katakana_response = await send_request(katakana_request)
        print(f"Katakana response: {katakana_response}")

        # Test roman conversion
        roman_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {"name": "convert_to_roman", "arguments": {"text": "こんにちは、世界！"}},
        }

        print("\nTesting roman conversion...")
        roman_response = await send_request(roman_request)
        print(f"Roman response: {roman_response}")

    except Exception as e:
        print(f"Error during testing: {e}")

    finally:
        # Clean up
        process.terminate()
        await process.wait()


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
