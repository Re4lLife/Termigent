"""Command-line entry point for Termigent."""

import argparse
import asyncio
import logging

import uvicorn

from termigent import __version__
from termigent.server import build_app

GREEN = "\033[32m"
RESET = "\033[0m"

_QUIET_LOGGERS = (
    "uvicorn",
    "uvicorn.error",
    "uvicorn.access",
    "mcp",
    "mcp.server",
    "mcp.server.sse",
    "anyio",
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="termigent",
        description="Universal MCP server exposing a system terminal over SSE.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Interface to bind (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to listen on (default: 8000)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def _silence_network_logs() -> None:
    for name in _QUIET_LOGGERS:
        logging.getLogger(name).setLevel(logging.CRITICAL)


async def _serve(host: str, port: int) -> None:
    config = uvicorn.Config(
        build_app(),
        host=host,
        port=port,
        log_config=None,
        access_log=False,
    )
    server = uvicorn.Server(config)
    task = asyncio.create_task(server.serve())

    while not server.started:
        if task.done():
            await task
            return
        await asyncio.sleep(0.05)

    print(f"{GREEN}Ready!{RESET}", flush=True)
    await task


def main(argv: list[str] | None = None) -> None:
    args = _parser().parse_args(argv)

    _silence_network_logs()

    print(
        f"🚀 Launching Termigent over SSE on http://{args.host}:{args.port}",
        flush=True,
    )

    try:
        asyncio.run(_serve(args.host, args.port))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
