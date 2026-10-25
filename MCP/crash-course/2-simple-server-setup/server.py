import sys

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator", port=8050)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


if __name__ == "__main__":
    transport = "streamable-http"
    if len(sys.argv) > 1:
        transport = sys.argv[1]

    print("Calculator server starting with transport:", transport, file=sys.stderr)
    mcp.run(transport=transport)
