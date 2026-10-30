import json
import os

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Knowledge Base")


@mcp.tool()
def get_knowledge_base() -> str:
    """Retrieve the company knowledge base, with every question and answer about company policies."""
    folder = os.path.dirname(__file__)
    kb_path = os.path.join(folder, "data", "kb.json")

    with open(kb_path) as f:
        kb_data = json.load(f)

    text = "Here is the retrieved knowledge base:\n\n"
    for item in kb_data:
        text += "Q: " + item["question"] + "\n"
        text += "A: " + item["answer"] + "\n\n"

    return text


if __name__ == "__main__":
    mcp.run(transport="stdio")
