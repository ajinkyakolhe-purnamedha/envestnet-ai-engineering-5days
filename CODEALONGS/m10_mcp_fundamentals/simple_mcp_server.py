import logging
import sys

from mcp.server import MCPServer


# In stdio mode, stdout belongs to MCP. Send logs to stderr and a file.
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("mcp-demo")

mcp = MCPServer("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """A tool is an action the client can call."""
    logger.info("add(%s, %s)", a, b)
    return a + b


@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """A resource is read-only data addressed by a URI."""
    logger.info("reading greeting for %s", name)
    return f"Hello, {name}! Welcome to MCP."


if __name__ == "__main__":
    logger.info("starting MCP server")
    mcp.run(transport="stdio")
