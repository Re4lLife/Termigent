"""MCP server definition and the terminal execution tool."""

import subprocess
import sys

from mcp.server.fastmcp import FastMCP

GREEN = "\033[32m"
WHITE = "\033[97m"
OUTPUT = "\033[38;5;252m"
RESET = "\033[0m"
PROMPT = f"{GREEN}agent@termigent:~$ {WHITE}"

mcp = FastMCP("termigent")


@mcp.tool()
def run_command(command: str) -> str:
    """Execute a shell command on the host terminal and return its output.

    Args:
        command: The shell command to execute.
    """
    print(f"{PROMPT}{command}{RESET}", flush=True)

    process = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    output = process.stdout or ""
    if output:
        sys.stdout.write(OUTPUT)
        sys.stdout.write(output)
        if not output.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.write(RESET)
        sys.stdout.flush()

    if process.returncode != 0:
        return f"{output}\n[exit code: {process.returncode}]"
    return output


def build_app():
    """Return the Starlette app exposing the SSE MCP endpoint."""
    return mcp.sse_app()
