Blink_MCPMock_app.py



"""
Flask + MCP (OpenAI Model Context Protocol) — compliant skeleton
Requires: mcp==1.21.0, flask, gunicorn (for deploy)
"""

import os
import threading
from flask import Flask, jsonify
from mcp.server.fastmcp import FastMCP  # <- correct import for mcp 1.21.0

# ------------------ Flask (HTTP) ------------------
app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({"ok": True, "message": "Flask + MCP is healthy"})

# ------------------ MCP (STDIO) -------------------
mcp = FastMCP("flask-mcp-server")  # server name (shown to clients)

# Minimal example tools (safe & serializable). You can remove if you want no tools.
@mcp.tool()
def ping() -> dict:
    """Simple MCP health check."""
    return {"pong": True}

@mcp.tool()
def add_numbers(a: int, b: int) -> dict:
    """Add two integers."""
    return {"sum": a + b}

def run_mcp_stdio():
    # Runs the MCP server on STDIO (the transport most MCP hosts expect)
    # Do not block the Flask thread; run as daemon thread.
    mcp.run_stdio()

# ------------------ Entry point -------------------
if __name__ == "__main__":
    # Start MCP stdio server in background
    threading.Thread(target=run_mcp_stdio, daemon=True).start()

    # Start Flask HTTP server
    port = int(os.getenv("PORT", 3333))
    app.run(host="0.0.0.0", port=port)
