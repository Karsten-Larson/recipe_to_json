import typer
import asyncio
import os
from pathlib import Path
from langchain_core.runnables import RunnableConfig
from ..agent import GraphState, agent

app = typer.Typer()

@app.command()
def main(
    url: str = typer.Argument(None, help="URL of the recipe website"),
    urls_file: typer.FileText = typer.Option(None, help="Path to text file with multiple URLs, one per line"),
    output_dir: str = typer.Option("./recipes", help="Output directory for recipes")
):
    if not url and not urls_file:
        typer.echo("Must provide either URL or --urls-file")
        raise typer.Exit(1)

    output_path = Path(output_dir)

    if url:
        state = GraphState(selected_url=url, output_path=output_path)
        asyncio.run(agent.ainvoke(state))

    if urls_file:
        urls = [line.strip() for line in urls_file if line.strip()]
        states = [GraphState(selected_url=u, output_path=output_path) for u in urls]
        config: RunnableConfig = {"max_concurrency": 5}
        asyncio.run(agent.abatch(states, config=config, return_exceptions=False))

@app.command()
def web(directory: str = typer.Option("./recipes", help="Directory containing recipe JSON files")):
    os.environ['RECIPES_DIR'] = directory

    try:
        from ..web.app import app
    except ImportError:
        typer.echo("Flask is not installed. Please install the 'web' extra to use this command.")
        raise typer.Exit(1)

    app.run(debug=True)

if __name__ == "__main__":
    app()

