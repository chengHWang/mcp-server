# test_stream.py
import requests
import json

resp = requests.post(
    "http://localhost:8000/streamable_http",
    headers={
        "Content-Type": "application/json",
        "x-mcp-sessionid": "sess_123"
    },
    json={
        "jsonrpc": "2.0",
        "method": "call_tool",
        "params": {
            "name": "count_down",
            "arguments": {"start": 2}
        },
        "id": "req_1"
    },
    stream=True
)

print("开始接收流式响应...")
for line in resp.iter_lines():
    if line:
        print(">>>", json.loads(line.decode()))