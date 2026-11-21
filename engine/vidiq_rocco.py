#!/usr/bin/env python3
"""vidiq_rocco.py - call vidIQ tools for the Red Flag Rocco profile (second vidIQ account).
The built-in vidIQ MCP tools in a session are logged into the Financier account. Rocco's account is reached
with the key in env VIDIQ_API_KEY (never printed, never written to the repo) through https://mcp.vidiq.com/mcp.

  python3 -I engine/vidiq_rocco.py vidiq_user_channels
  python3 -I engine/vidiq_rocco.py vidiq_balance
  python3 -I engine/vidiq_rocco.py vidiq_keyword_research '{"keyword": "phone scams"}'
  python3 -I engine/vidiq_rocco.py --list            # tool names

Same tool names and arguments as the built-in vidIQ tools; credits come from Rocco's account.
"""
import json, os, subprocess, sys

URL = "https://mcp.vidiq.com/mcp"


def call(method, params, rid=1):
    key = os.environ.get("VIDIQ_API_KEY") or sys.exit("VIDIQ_API_KEY not set")
    body = json.dumps({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
    r = subprocess.run(["curl", "-sS", "--max-time", "180", URL, "-H", "Authorization: Bearer " + key,
                        "-H", "Content-Type: application/json", "-H", "Accept: application/json, text/event-stream",
                        "--data-binary", "@-"], input=body.encode(), capture_output=True, check=True)
    out = r.stdout.decode()
    for line in out.splitlines():
        if line.startswith("data: "):
            return json.loads(line[6:])
    return json.loads(out)


def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    if sys.argv[1] == "--list":
        res = call("tools/list", {})
        print("\n".join(t["name"] for t in res["result"]["tools"])); return
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    res = call("tools/call", {"name": sys.argv[1], "arguments": args})
    if "error" in res: sys.exit("vidiq error: " + json.dumps(res["error"])[:800])
    r = res["result"]
    print(json.dumps(r.get("structuredContent") or r.get("content"), indent=1, ensure_ascii=False)[:20000])


if __name__ == "__main__":
    main()
