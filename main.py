import re
import requests

API_KEY = "ATvMswvlAHJvostqtYkGnpuoNO38y16F"

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def search_ingredients(query, sort_direction=None, sort=None, offset=None, number=None, intolerances=None):
    url = "https://api.spoonacular.com/food/ingredients/search"

    params = {
        'query': query,
        'sortDirection': sort_direction,
        'sort': sort,
        'offset': offset,
        'number': number,
        'intolerances': intolerances,
        'apiKey': API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def search_recipes(query, number=5):
    url = "https://api.spoonacular.com/recipes/search"

    params = {
        'query': query,
        'number': number,
        'apiKey': API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def get_recipe_info(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"

    params = {
        'apiKey': API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response("recipe", ["recipe"])
    # Add other predefined messages and corresponding lists of words here

    if "recipe" in highest_prob_list:
        recipe_query = input("BOT: Please enter the name of the dish you want the recipe for: ")
        recipes = search_recipes(recipe_query)

        if recipes and 'results' in recipes:
            print(f"BOT: Here are some recipes for {recipe_query}:")
            for i, recipe in enumerate(recipes['results'], start=1):
                print(f"{i}. {recipe['title']} (ID: {recipe['id']})")

            selected_recipe_index = int(input("BOT: Enter the number of the recipe you want more information about: "))
            selected_recipe = recipes['results'][selected_recipe_index - 1]

            recipe_info = get_recipe_info(selected_recipe['id'])

            if recipe_info:
                print(f"BOT: Recipe Information for {selected_recipe['title']}:")
                print(f" - Ingredients:")
                for ingredient in recipe_info['extendedIngredients']:
                    print(f"   - {ingredient['originalString']}")

                print(f" - Calories: {recipe_info['nutrition']['nutrients'][0]['amount']} kcal")
                print(f" - Fat Percentage: {recipe_info['nutrition']['nutrients'][1]['percentOfDailyNeeds']}%")
            else:
                print(f"BOT: Sorry, I don't have information on the recipe with ID {selected_recipe['id']}.")

        else:
            print(f"BOT: Sorry, I couldn't find any recipes for {recipe_query}.")

    # Add more conditions and responses based on recognized words

while True:
    user_input = input('You:')
    if user_input.lower() == 'exit':
        break
    check_all_messages(re.split(r'\s+|[,;?!.-]\s*', user_input.lower()))
