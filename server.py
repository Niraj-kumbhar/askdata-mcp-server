from fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
import yaml
import pathlib

mcp = FastMCP("db-metadata-server")

METADATA_DIR = pathlib.Path("metadata")

# ── Tool 1: List all tables ──────────────────────────────────────
@mcp.tool()
def list_tables() -> str:
    """Returns all available tables with a short description."""
    tables = []
    for f in METADATA_DIR.glob("*.yaml"):
        data = yaml.safe_load(f.read_text())
        name = f.stem
        desc = data.get("description", "No description")
        tables.append(f"- {name}: {desc}")
    return "\n".join(tables) if tables else "No tables found."

# ── Tool 2: Get table details ────────────────────────────────────
@mcp.tool()
def get_tables(table_names: list[str]) -> str:
    """Returns full schema info for the given list of table names."""
    results = []
    for name in table_names:
        path = METADATA_DIR / f"{name}.yaml"
        if path.exists():
            results.append(f"### {name}\n{path.read_text()}")
        else:
            results.append(f"### {name}\n[Not found]")
    return "\n\n".join(results)

# # ── Tool 3: Run SELECT-only SQL ──────────────────────────────────
# @mcp.tool()
# def run_sql(query: str) -> str:
#     """Executes a read-only SELECT query against the database."""
#     q = query.strip().lower()
#     if not q.startswith("select"):
#         return "Error: Only SELECT queries are permitted."
    
#     # TODO: replace with your actual DB connection
#     # import sqlite3
#     # conn = sqlite3.connect("mydb.db")
#     # rows = conn.execute(query).fetchall()
#     # return str(rows)
#     return f"[Stub] Would run: {query}"

# if __name__ == "__main__":
#     mcp.run(transport="http", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    import uvicorn

    # Get the underlying Starlette app from FastMCP and add CORS
    app = mcp.http_app(path="/mcp", stateless_http=True)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],          # tighten in production
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)