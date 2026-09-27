"""Stdio MCP adapter on the Pi; forwards tools over an authenticated SSH tunnel."""
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen

BASE = os.environ.get("OBI_PC_URL", "http://127.0.0.1:4317")
TOKEN_FILE = Path(os.environ.get("OBI_PC_TOKEN_FILE", str(Path.home() / ".openfang/obi-pc.token")))


def remote(endpoint, payload):
    req = Request(BASE + endpoint, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", "Authorization": "Bearer " + TOKEN_FILE.read_text().strip()})
    with urlopen(req, timeout=45) as response:
        result = json.load(response)
    if "error" in result:
        raise ValueError(result["error"])
    return result["result"]


def handle(message):
    method = message.get("method")
    if method == "initialize":
        return {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "obi-pc", "version": "1.0.0"}}
    if method == "tools/list":
        # Local schema remains discoverable when the PC is temporarily offline.
        return json.loads(Path(__file__).with_name("tools.json").read_text())
    if method == "tools/call":
        try:
            result = remote("/call", message["params"])
            if isinstance(result, dict) and isinstance(result.get("content"), list):
                # OpenFang 0.6.9 serializes image-only MCP results into a text
                # tool result, wasting tokens on base64 without enabling vision.
                blocks = result['content']
                if any(b.get('type') == 'image' for b in blocks):
                    result = {**result, 'content': [b for b in blocks if b.get('type') != 'image'] + [
                        {'type': 'text', 'text': json.dumps({
                            'visual_review_available': False,
                            'reason': 'OpenFang 0.6.9 MCP results are text-only. Image bytes omitted; do not claim to have seen it. Request human review of the saved image.',
                            'artifact': message['params'].get('arguments', {}).get('path'),
                            'image_count': sum(b.get('type') == 'image' for b in blocks)
                        })}
                    ]}
                return result
            return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}], "isError": False}
        except Exception as exc:
            return {"content": [{"type": "text", "text": "PC tool failed: " + str(exc)}], "isError": True}
    if method == "ping":
        return {}
    raise ValueError("Unknown MCP method")


def main():
    for line in sys.stdin:
        try:
            message = json.loads(line)
            if "id" not in message:
                continue
            try:
                reply = {"jsonrpc": "2.0", "id": message["id"], "result": handle(message)}
            except Exception as exc:
                reply = {"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32603, "message": str(exc)}}
            print(json.dumps(reply, ensure_ascii=False), flush=True)
        except json.JSONDecodeError:
            continue


if __name__ == '__main__':
    main()
