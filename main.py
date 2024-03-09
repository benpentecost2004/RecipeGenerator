import requests

API_ENDPOINT = "https://api.spoonacular.com/recipes/findByIngredients"


def fetch_recipes(ingredients, api_key, ):
    params = {
        "ingredients": ",".join(ingredients),
        "number": 5,
        "apiKey": api_key,
        # "diet": ",".join(dietary_restrictions)
    }
    response = requests.get(API_ENDPOINT, params=params)
    if response.status_code == 200:
        recipes = response.json()
        for recipe in recipes:
            recipe["missing_ingredients"] = get_missing_ingredients(recipe["missedIngredients"])
        return recipes
    else:
        print("Failed to fetch recipes:", response.status_code)
        return []


def get_missing_ingredients(missed_ingredients):
    return [ingredient["name"] for ingredient in missed_ingredients]


def main():
    print("Welcome to Recipe Generator!")
    print("Please enter the ingredients you have (separated by commas):")
    user_input = input().strip().lower()
    available_ingredients = [ingredient.strip() for ingredient in user_input.split(",")]

    # print("Do you have any dietary restrictions? (e.g., vegetarian, vegan, gluten free)")
    # dietary_restrictions = input().strip().lower().split(",")

    api_key = 'd55ef8798a254dda9dffeed66d1e205a'
    recipes = fetch_recipes(available_ingredients, api_key)

    if recipes:
        print("You can make the following recipes:")
        for recipe in recipes:
            print("-", recipe['title'])
            if recipe["missing_ingredients"]:
                print("  Additional Ingredients Needed:", ", ".join(recipe["missing_ingredients"]))
            else:
                print("  You have all the ingredients!")
    else:
        print("Sorry, you don't have enough ingredients to make any recipe.")


if __name__ == "__main__":
    main()
