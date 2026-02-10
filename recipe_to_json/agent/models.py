from pydantic import BaseModel, Field

class Ingredient(BaseModel):
    """Represents an ingredient with its name, quantity, and unit of measurement."""
    name: str = Field(description="The name of the ingredient")
    quantity: str = Field(description="The amount needed")
    unit: str = Field(description="The unit of measurement")


class Step(BaseModel):
    """Represents a single step in the recipe with its number and instruction."""
    number: int = Field(description="The step number")
    instruction: str = Field(description="The instruction for this step")


class Time(BaseModel):
    """Represents the time details for the recipe, including preparation, cooking, and total time."""
    prep_time: str = Field(description="Preparation time")
    cook_time: str = Field(description="Cooking time")
    total_time: str = Field(description="Total time required")


class Recipe(BaseModel):
    """Represents a complete recipe with all its details."""
    title: str = Field(description="The name of the dish")
    image_url: str | None = Field(default=None, description="URL of the recipe image")
    time: Time = Field(description="Time details for the recipe")
    serves: int = Field(default=1, description="Number of people the recipe serves")
    ingredients: list[Ingredient] = Field(description="List of required ingredients with measurements")
    steps: list[Step] = Field(description="Numbered preparation steps")
    notes: list[str] = Field(description="Extra tips or substitutions")