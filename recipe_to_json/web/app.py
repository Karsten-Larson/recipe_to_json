from flask import Flask, render_template, request, redirect, url_for
import json
import os
from pathlib import Path
from ..agent import GraphState, agent
from langchain_core.runnables import RunnableConfig
import asyncio

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

RECIPES_DIR = os.environ.get('RECIPES_DIR', './recipes')

@app.route('/')
def index():
    recipes = []
    if os.path.exists(RECIPES_DIR):
        for file in os.listdir(RECIPES_DIR):
            if file.endswith('.json'):
                filepath = os.path.join(RECIPES_DIR, file)
                try:
                    with open(filepath) as f:
                        data = json.load(f)
                        recipes.append({
                            'title': data.get('title', file),
                            'file': file,
                            'serves': data.get('serves'),
                            'steps_count': len(data.get('steps', [])),
                            'image_url': data.get('image_url'),
                            'prep_time': data.get('time', {}).get('prep_time'),
                            'cook_time': data.get('time', {}).get('cook_time'),
                            'total_time': data.get('time', {}).get('total_time')
                        })
                except:
                    pass
    return render_template('index.html', recipes=recipes)

@app.route('/add_recipes', methods=['POST'])
def add_recipes():
    urls_text = request.form.get('urls', '')
    urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
    if urls:
        output_path = Path(RECIPES_DIR)
        states = [GraphState(selected_url=url, output_path=output_path) for url in urls]
        config: RunnableConfig = {"max_concurrency": 5}
        asyncio.run(agent.abatch(states, config=config, return_exceptions=False))
    return redirect(url_for('index'))

@app.route('/recipe/<filename>')
def recipe(filename):
    filepath = os.path.join(RECIPES_DIR, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath) as f:
                data = json.load(f)
            return render_template('recipe.html', recipe=data)
        except:
            return "Error loading recipe", 500
    return "Recipe not found", 404

if __name__ == '__main__':
    app.run(debug=True)