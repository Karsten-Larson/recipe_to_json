from pydantic import BaseModel, Field
from curl_cffi.requests import AsyncSession
from markitdown import FileConversionException, MarkItDown
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

from io import BytesIO
from pathlib import Path
from functools import partial

from .models import Recipe

# Load environment variables from .env file
import dotenv

dotenv.load_dotenv()

# Define the LLM (can be used in multiple nodes)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

# Define the state of the graph
class GraphState(BaseModel):
    selected_url: str
    markdown_content: str | None = None
    final_recipe: Recipe | None = None
    output_path: Path = Field(default=Path("recipes"), description="Directory to save the final recipe JSON files")

async def download_node(state: GraphState):
    async with AsyncSession() as s:
        response = await s.get(
            state.selected_url, 
            impersonate="chrome",
            timeout=15
        )

    if response.status_code != 200:
        print(f"--- Failed to download {state.selected_url}: {response.status_code} ---")
        # You can either raise an error or return an empty state to be caught by a conditional edge
        return {"markdown_content": None}

    md = MarkItDown()

    try:
        # MarkItDown can convert directly from a URL
        result = md.convert(BytesIO(response.content))
    except FileConversionException:
        print(f"--- Conversion failed for {state.selected_url} ---")
        return {"markdown_content": None}

    return {"markdown_content": result.text_content}


def extraction_node(state: GraphState):
    structured_llm = llm.with_structured_output(Recipe)

    content = state.markdown_content

    if not content:
        print(f"--- No markdown content to extract from {state.selected_url} ---")
        return {"final_recipe": None}
    
    prompt = f"Extract the recipe details from this markdown content:\n\n{content}"
    recipe_object = structured_llm.invoke(prompt)
    
    return {"final_recipe": recipe_object}


def save_node(state: GraphState):
    recipe = state.final_recipe
    output_path = state.output_path

    if not recipe:
        print(f"--- No recipe to save for {state.selected_url} ---")
        return {}
    
    # Create a filename based on the title
    filename = output_path / f"{recipe.title.replace(' ', '_').lower()}.json"
    
    # Ensure directory exists
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save the Pydantic model as JSON
    with open(filename, "w") as f:
        f.write(recipe.model_dump_json(indent=4))
    
    print(f"--- Recipe saved to {filename} ---")
    return {}

# Conditional functions to determine the next node
def should_proceed_to(node: str, state: GraphState):
    return node if state.markdown_content is not None else END

should_proceed_to_extract = partial(should_proceed_to, "extract")
should_proceed_to_save = partial(should_proceed_to, "save")

# Define the workflow graph
workflow = StateGraph(GraphState)

workflow.add_node("download", download_node)
workflow.add_node("extract", extraction_node)
workflow.add_node("save", save_node)

workflow.set_entry_point("download")
workflow.add_conditional_edges("download", should_proceed_to_extract)
workflow.add_conditional_edges("extract", should_proceed_to_save)
workflow.add_edge("save", END)

agent = workflow.compile()