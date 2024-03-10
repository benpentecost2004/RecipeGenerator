import requests

API_ENDPOINT = "https://api.spoonacular.com/recipes/findByIngredients"


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
            recipe["missing_ingredients"] = get_missing_ingredients(recipe["missedIngredients"])
            recipe["source_url"] = get_source_url(recipe["id"], api_key)
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
        return data["sourceUrl"]
    else:
        return "Source URL not available"


def main():
    print("Welcome to Recipe Generator!")
    print("Please enter the ingredients you have (separated by commas):")
    user_input = input().strip().lower()
    available_ingredients = [ingredient.strip() for ingredient in user_input.split(",")]

    api_key = '869cb16aba7a44688ea0a366b4b5bb45'
    recipes = fetch_recipes(available_ingredients, api_key)

    if recipes:
        print("You can make the following recipes:")
        for recipe in recipes:
            print("-", recipe['title'])
            if recipe["missing_ingredients"]:
                print("  Additional Ingredients Needed:", ", ".join(recipe["missing_ingredients"]))
            else:
                print("  You have all the ingredients!")
            print("  Recipe Source URL:", recipe["source_url"])
    else:
        print("Sorry, you don't have enough ingredients to make any recipe.")


if __name__ == "__main__":
    main()
