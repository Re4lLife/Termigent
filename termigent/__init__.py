"""Termigent - a universal MCP server exposing a system terminal over SSE."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("termigent")
except PackageNotFoundError:
    __version__ = "0.0.0"
