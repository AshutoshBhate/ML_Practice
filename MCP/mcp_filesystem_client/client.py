"""
MCP Filesystem Client (stdio transport)
----------------------------------------
Connects to the official @modelcontextprotocol/server-filesystem Node.js server
as a subprocess and calls its tools from pure Python.

Prerequisites:
    pip install mcp
    npm install -g @modelcontextprotocol/server-filesystem   # or use npx (no install needed)

Usage:
    python client.py
"""

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ── Configuration ─────────────────────────────────────────────────────────────

# The directory you want the filesystem server to have access to.
# Change this to any absolute path on your machine.
ALLOWED_DIR = os.path.expanduser("~/mcp_sandbox")

# Server launch parameters – we use npx so no global npm install is needed.
SERVER_PARAMS = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", ALLOWED_DIR],
)


# ── Helper ─────────────────────────────────────────────────────────────────────

async def call(session: ClientSession, tool: str, **kwargs):
    """Thin wrapper: call a tool and return the first text result."""
    result = await session.call_tool(tool, arguments=kwargs)
    # result.content is a list of TextContent / BlobContent blocks
    texts = [block.text for block in result.content if hasattr(block, "text")]
    return "\n".join(texts)


# ── Demo ───────────────────────────────────────────────────────────────────────

async def main():
    # Make sure the sandbox directory exists
    os.makedirs(ALLOWED_DIR, exist_ok=True)

    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:

            # 1. Handshake
            await session.initialize()
            print("✅ Connected to MCP filesystem server\n")

            # 2. Discover available tools
            tools_response = await session.list_tools()
            print("🔧 Available tools:")
            for tool in tools_response.tools:
                print(f"   • {tool.name}: {tool.description}")
            print()

            # ── Write a file ──────────────────────────────────────────────────
            file_path = os.path.join(ALLOWED_DIR, "hello.txt")
            print(f"📝 Writing file: {file_path}")
            result = await call(
                session,
                "write_file",
                path=file_path,
                content="Hello from Python MCP client!\nLine 2 here.\n",
            )
            print(f"   → {result}\n")

            # ── Read the file back ────────────────────────────────────────────
            print(f"📖 Reading file: {file_path}")
            content = await call(session, "read_file", path=file_path)
            print(f"   → {repr(content)}\n")

            # ── List the directory ────────────────────────────────────────────
            print(f"📂 Listing directory: {ALLOWED_DIR}")
            listing = await call(session, "list_directory", path=ALLOWED_DIR)
            print(f"   → {listing}\n")

            # ── Create a subdirectory ─────────────────────────────────────────
            sub_dir = os.path.join(ALLOWED_DIR, "subdir")
            print(f"📁 Creating directory: {sub_dir}")
            result = await call(session, "create_directory", path=sub_dir)
            print(f"   → {result}\n")

            # ── Move (rename) the file ────────────────────────────────────────
            new_path = os.path.join(sub_dir, "hello_moved.txt")
            print(f"🚚 Moving {file_path} → {new_path}")
            result = await call(
                session, "move_file", source=file_path, destination=new_path
            )
            print(f"   → {result}\n")

            # ── Search for files ──────────────────────────────────────────────
            print(f"🔍 Searching for '*.txt' under {ALLOWED_DIR}")
            found = await call(
                session, "search_files", path=ALLOWED_DIR, pattern="*.txt"
            )
            print(f"   → {found}\n")

            # ── Get file metadata ─────────────────────────────────────────────
            print(f"ℹ️  File info for: {new_path}")
            info = await call(session, "get_file_info", path=new_path)
            print(f"   → {info}\n")

            print("✅ Demo complete!")


if __name__ == "__main__":
    asyncio.run(main())