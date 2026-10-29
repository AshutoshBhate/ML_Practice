import json

import httpx

url = "http://127.0.0.1:8060/mcp"
headers = {"Accept": "application/json, text/event-stream"}


def read_message(response):
    for line in response.text.splitlines():
        if line.startswith("data: "):
            return json.loads(line[len("data: "):])


initialize = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-11-25",
        "capabilities": {},
        "clientInfo": {"name": "probe", "version": "1.0"},
    },
}
response = httpx.post(url, json=initialize, headers=headers)
server_info = read_message(response)["result"]["serverInfo"]
print("initialize:", response.status_code, server_info["name"])

headers["Mcp-Session-Id"] = response.headers["Mcp-Session-Id"]
headers["MCP-Protocol-Version"] = "2025-11-25"

response = httpx.post(url, json={"jsonrpc": "2.0", "method": "notifications/initialized"}, headers=headers)
print("notifications/initialized:", response.status_code)

response = httpx.post(url, json={"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, headers=headers)
tool_names = []
for tool in read_message(response)["result"]["tools"]:
    tool_names.append(tool["name"])
print("tools/list:", response.status_code, tool_names)

httpx.delete(url, headers=headers)

if response.status_code == 200 and "convert_time" in tool_names:
    print("PASS")
else:
    print("FAIL")
