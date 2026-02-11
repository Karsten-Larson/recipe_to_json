from pydantic import computed_field
from flask import Flask, render_template, request, redirect, url_for
import os
from pathlib import Path
from ..agent import GraphState, agent
from ..models import Recipe
from langchain_core.runnables import RunnableConfig
import asyncio

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

RECIPES_DIR = Path(os.environ.get('RECIPES_DIR', './recipes'))

class RecipeResponse(Recipe):
    file: str
    
    @computed_field
    @property
    def steps_count(self) -> int:
        return len(self.steps) if self.steps else 0

@app.route('/')
def index():
    recipes: list[RecipeResponse] = []

    if not RECIPES_DIR.exists():
        return render_template('index.html', recipes=recipes)
    
    for file_path in RECIPES_DIR.glob('*.json'):
        try:
            with open(file_path) as f:
                raw_recipe = Recipe.model_validate_json(f.read())
                recipes.append(RecipeResponse(**raw_recipe.model_dump(), file=file_path.name))
        except:
            pass
    return render_template('index.html', recipes=recipes)

@app.route('/add_recipes', methods=['POST'])
def add_recipes():
    urls_text = request.form.get('urls', '')
    urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
    if urls:
        states = [GraphState(selected_url=url, output_path=RECIPES_DIR) for url in urls]
        config: RunnableConfig = {"max_concurrency": 5}
        asyncio.run(agent.abatch(states, config=config, return_exceptions=False))
        return redirect(url_for('index', success='1'))
    return redirect(url_for('index'))

@app.route('/recipe/<filename>')
def recipe(filename):
    filepath = RECIPES_DIR / filename
    if filepath.exists():
        try:
            with open(filepath) as f:
                data = Recipe.model_validate_json(f.read())
            return render_template('recipe.html', recipe=data)
        except:
            return "Error loading recipe", 500
    return "Recipe not found", 404

if __name__ == '__main__':
    app.run(debug=True)