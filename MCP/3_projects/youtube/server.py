import re

from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

mcp = FastMCP("YouTube")
api = YouTubeTranscriptApi()


def extract_video_id(url_or_id):
    match = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([0-9A-Za-z_-]{11})", url_or_id)
    if match:
        return match.group(1)
    return url_or_id


@mcp.tool()
def get_transcript(video_url_or_id: str) -> str:
    """Get the transcript of a YouTube video as plain text, from its URL or its 11-character video ID."""
    video_id = extract_video_id(video_url_or_id)
    transcript = api.fetch(video_id)
    return TextFormatter().format_transcript(transcript)


if __name__ == "__main__":
    mcp.run(transport="stdio")
