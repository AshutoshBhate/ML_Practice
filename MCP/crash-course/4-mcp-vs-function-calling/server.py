from mcp.server.fastmcp import FastMCP

from tools import add

mcp = FastMCP("Calculator")
mcp.add_tool(add)

if __name__ == "__main__":
    mcp.run(transport="stdio")
