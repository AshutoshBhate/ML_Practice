from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator", host="0.0.0.0", port=8050)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
