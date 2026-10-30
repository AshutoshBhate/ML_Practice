import sqlite3
import sys
from contextlib import asynccontextmanager

from mcp.server.mcpserver import Context, MCPServer


@asynccontextmanager
async def lifespan(server):
    print("Startup: Opening the database", file=sys.stderr)
    db = sqlite3.connect(":memory:", check_same_thread=False)
    db.execute("CREATE TABLE notes (text TEXT)")
    db.execute("INSERT INTO notes VALUES ('Standup at 10'), ('Demo on Friday')")

    try:
        yield {"db": db}
    finally:
        db.close()
        print("Shutdown: Closed the database", file=sys.stderr)


mcp = MCPServer("Notes", lifespan=lifespan)


@mcp.tool()
def count_notes(ctx: Context) -> int:
    """Count the notes in the database"""
    db = ctx.request_context.lifespan_context["db"]
    row = db.execute("SELECT COUNT(*) FROM notes").fetchone()
    return row[0]


@mcp.tool()
def add_note(text: str, ctx: Context) -> str:
    """Add a note to the database"""
    db = ctx.request_context.lifespan_context["db"]
    db.execute("INSERT INTO notes VALUES (?)", (text,))
    return "Added: " + text


if __name__ == "__main__":
    mcp.run(transport="stdio")
