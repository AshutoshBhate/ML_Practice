from mcp.server.mcpserver import MCPServer

from tools import add

mcp = MCPServer("Calculator")
mcp.add_tool(add)

if __name__ == "__main__":
    mcp.run(transport="stdio")
