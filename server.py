from pathlib import Path
import json
from mcp.server.fastmcp import FastMCP

server = FastMCP("inventory")

@server.tool()
def get_stock(sku: str) -> dict:
    """Read stock for an exact SKU from the bundled inventory fixture."""
    stock = json.loads((Path(__file__).parent / "data/input.json").read_text())["stock"]
    if sku not in stock:
        raise ValueError("Unknown SKU")
    return {"sku": sku, "units": stock[sku]}

if __name__ == "__main__":
    server.run(transport="stdio")
