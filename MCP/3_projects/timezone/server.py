import os
from datetime import datetime
from zoneinfo import ZoneInfo

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Timezone")

offices = {
    "Pune": "Asia/Kolkata",
    "London": "Europe/London",
    "New York": "America/New_York",
}


@mcp.tool()
def convert_time(time: str, from_zone: str, to_zone: str) -> str:
    """Convert a time from one time zone to another. time is "YYYY-MM-DD HH:MM", and the zones are IANA names like "Asia/Kolkata"."""
    start = datetime.strptime(time, "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo(from_zone))
    converted = start.astimezone(ZoneInfo(to_zone))
    return converted.strftime("%Y-%m-%d %H:%M %Z")


@mcp.resource("zones://offices")
def get_offices() -> str:
    """Our offices and their IANA time zones."""
    lines = []
    for city, zone in offices.items():
        lines.append(city + ": " + zone)
    return "\n".join(lines)


@mcp.prompt()
def plan_meeting(date: str, time: str) -> str:
    """Ask what a meeting at a given Pune time is in every office, and whether it falls in working hours."""
    return f"We want a meeting on {date} at {time} Pune time. Use the convert_time tool to find its local time in every office, and say whether it falls inside working hours, 09:00 to 18:00 local time."


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host=os.getenv("HOST", "127.0.0.1"), port=8060)
