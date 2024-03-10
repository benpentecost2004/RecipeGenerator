from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_ENDPOINT = "https://api.spoonacular.com/recipes/findByIngredients"
API_KEY = '4e965940d8064245b4ada8f022098a8c'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes', methods=['POST'])
def get_recipes():
    ingredients = request.form.get('ingredients').split(',')
    recipes = fetch_recipes(ingredients, API_KEY)

    if recipes:
        return render_template('recipes.html', recipes=recipes)
    else:
        return "Sorry, no recipes found with the given ingredients."

def fetch_recipes(ingredients, api_key):
    params = {
        "ingredients": ", ".join(ingredients),
        "number": 5,
        "apiKey": api_key,
    }
    response = requests.get(API_ENDPOINT, params=params)
    if response.status_code == 200:
        recipes = response.json()
        for recipe in recipes:
            recipe["missing_ingredients"] = get_missing_ingredients(recipe.get("missedIngredients", []))
            recipe["source_url"] = get_source_url(recipe.get("id", ""), api_key)
            recipe["nutrients"] = get_nutrient_info(recipe.get("id", ""), api_key)
        return recipes
    else:
        print("Failed to fetch recipes:", response.status_code)
        return []

def get_missing_ingredients(missed_ingredients):
    return [ingredient["name"] for ingredient in missed_ingredients]

def get_source_url(recipe_id, api_key):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": api_key,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("sourceUrl", "Source URL not available")
    else:
        return "Source URL not available"

def get_nutrient_info(recipe_id, api_key):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    params = {
        "apiKey": api_key,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        nutrients = {}
        for nutrient in data.get("bad", []):
            nutrients[nutrient["title"]] = nutrient["amount"]
        for nutrient in data.get("good", []):
            nutrients[nutrient["title"]] = nutrient["amount"]
        return nutrients
    else:
        return {}

def fetch_recipes(ingredients, api_key):
    params = {
        "ingredients": ",".join(ingredients),
        "number": 5,
        "apiKey": api_key,
    }
    response = requests.get(API_ENDPOINT, params=params)
    if response.status_code == 200:
        recipes = response.json()
        for recipe in recipes:
            recipe["missing_ingredients"] = get_missing_ingredients(recipe.get("missedIngredients", []))
            recipe["source_url"] = get_source_url(recipe.get("id", ""), api_key)
            recipe["nutrients"] = get_nutrient_info(recipe.get("id", ""), api_key)
            recipe["image_url"] = get_image_url(recipe.get("id", ""), api_key)
        return recipes
    else:
        print("Failed to fetch recipes:", response.status_code)
        return []

def get_image_url(recipe_id, api_key):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": api_key,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("image", "")
    else:
        return ""


if __name__ == '__main__':
    app.run(debug=True)







