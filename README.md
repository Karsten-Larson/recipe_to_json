# Recipe to JSON

A command-line tool that converts recipe websites into structured JSON format using AI-powered parsing.

## Features

- Extract recipes from any recipe website URL
- Convert web content to structured JSON with ingredients, steps, and metadata
- Uses Google Gemini AI for accurate recipe parsing
- Supports batch processing of multiple URLs
- Outputs clean, machine-readable JSON files
- **Optional web interface** for viewing and managing recipes

## Installation

### Prerequisites

- Python 3.12 or higher
- Google AI API key (for Gemini model)

### Install Package

```bash
pip install recipe_to_json
# or with uv
uv pip install recipe_to_json
```

### Install with Web Interface

To use the optional web interface:

```bash
pip install recipe_to_json[web]
# or with uv
uv pip install recipe_to_json[web]
```

## Configuration

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Add your Google AI API key to `.env`:

   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

   Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Usage

### Basic Usage

Extract a single recipe:

```bash
recipe_to_json "https://example.com/recipe-url"
```

### Batch Processing

Process multiple URLs from a file:

```bash
recipe_to_json --urls-file urls.txt
```

### Options

- `url`: URL of the recipe website (required if not using --urls-file)
- `--urls-file`: Path to text file with one URL per line
- `--output-dir`: Output directory for JSON files (default: ./recipes)

### Examples

```bash
# Single recipe
recipe_to_json "https://cooking.nytimes.com/recipes/1026790-crispy-chicken-with-lime-butter"

# Batch processing
echo "https://example.com/recipe1" > urls.txt
echo "https://example.com/recipe2" >> urls.txt
recipe_to_json --urls-file urls.txt --output-dir ./my-recipes
```

## Web Interface

The package includes an optional web interface for viewing and managing your recipe collection.

### Installation

Install with web dependencies:

```bash
uv sync --extra web
```

### Running the Web Interface

Start the web server:

```bash
recipe_to_json web --directory ./recipes
```

The web interface will be available at `http://127.0.0.1:5000`.

### Features

- **Recipe Gallery**: View all your recipes in a responsive card grid
- **Recipe Details**: Click any recipe to see full details including ingredients, steps, and notes
- **Add New Recipes**: Use the "Add Recipes" button to download new recipes directly from URLs
- **Batch Processing**: Enter multiple URLs at once for batch downloading
- **Responsive Design**: Works on desktop and mobile devices

### Web Interface Usage

1. **View Recipes**: Browse your recipe collection on the main page
2. **Add Recipes**: Click the green "Add Recipes" button to open a modal
3. **Enter URLs**: Paste recipe URLs (one per line) and click "Add Recipes"
4. **Automatic Processing**: The system will download and parse the recipes using the same AI-powered extraction
5. **Success Notification**: Get alerted when recipes are successfully added

The web interface provides a user-friendly way to manage your recipe collection without using the command line.

## Output Format

The tool generates JSON files with the following structure:

```json
{
  "title": "Crispy Chicken with Lime Butter",
  "image_url": "https://example.com/image.jpg",
  "time": {
    "prep_time": "15 minutes",
    "cook_time": "30 minutes",
    "total_time": "45 minutes"
  },
  "serves": 4,
  "ingredients": [
    {
      "name": "Chicken breasts",
      "quantity": "4",
      "unit": "pieces"
    }
  ],
  "steps": [
    {
      "number": 1,
      "instruction": "Preheat oven to 400°F..."
    }
  ]
}
```

## How It Works

1. Downloads the recipe webpage using curl-cffi for reliable scraping
2. Converts HTML content to Markdown using MarkItDown
3. Uses Google Gemini AI to parse the recipe into structured data
4. Validates and saves the result as JSON

## Development

### Setup

```bash
uv sync
```

### Project Structure

```
recipe_to_json/
├── cli/
│   └── cli.py          # CLI interface
├── agent/
│   ├── __init__.py
│   ├── agent.py        # LangGraph agent logic
│   └── models.py       # Pydantic models
.env.example            # Environment template
```

## Dependencies

- `langchain` - AI orchestration
- `langchain-google-genai` - Google Gemini integration
- `markitdown` - HTML to Markdown conversion
- `curl-cffi` - Reliable HTTP requests
- `pydantic` - Data validation
- `typer` - CLI framework
- `flask` - Web interface (optional)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

GPL v3 License

This project is licensed under the terms of the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
MIT License
