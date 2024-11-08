import openai
import json
from difflib import get_close_matches
import os
from dotenv import load_dotenv

load_dotenv() 
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define categories from dataset
RECIPE_CATEGORIES = [
    "frozen desserts", "chicken breast", "beverages", "soy/tofu", "vegetable",
    "pie", "chicken", "dessert", "southwestern u.s.", "sauces", "stew",
    "black beans", "lactose free", "weeknight", "yeast breads", "whole chicken",
    "high protein", "cheesecake", "brazilian", "breakfast", "breads",
    "bar cookie", "brown rice", "oranges", "pork", "low protein", "asian",
    "potato", "cheese", "halibut", "meat", "lamb/sheep", "very low carbs",
    "pasta shells", "scones", "drop cookies", "lunch/snacks", "beans",
    "punch beverage", "pineapple", "low cholesterol", "quick breads",
    "sourdough breads", "curries", "chicken livers", "coconut", "savory pies",
    "poultry", "steak", "healthy", "lobster", "rice", "apple", "broil/grill",
    "spreads", "crab", "jellies", "pears", "chowders", "cauliflower", "candy",
    "chutneys", "white rice", "tex mex", "bass", "german", "fruit", "european",
    "smoothies", "hungarian", "manicotti", "onions", "new zealand",
    "chicken thigh & leg", "indonesian", "greek", "corn", "lentil", "summer",
    "long grain rice", "spanish", "dutch", "gelatin", "tuna", "citrus",
    "berries", "peppers", "salad dressings", "clear soup", "mexican",
    "raspberries", "crawfish", "beef organ meats", "strawberry", "shakes",
    "short grain rice", "one dish meal", "spicy", "thai", "cajun", "oven",
    "microwave", "russian", "melons", "swiss", "papaya", "veal", "no cook",
    "roast", "potluck", "orange roughy", "canadian", "caribbean", "mussels",
    "medium grain rice", "japanese", "penne", "easy", "elk", "colombian",
    "gumbo", "roast beef", "perch", "vietnamese", "rabbit", "christmas",
    "lebanese", "turkish", "kid friendly", "vegan", "for large groups",
    "whole turkey", "chinese", "grains", "yam/sweet potato", "native american",
    "meatloaf", "winter", "trout", "african", "ham", "goose", "stocks",
    "meatballs", "whole duck", "scandinavian", "greens", "catfish",
    "dehydrator", "duck breasts", "savory", "stir fry", "polish", "spring",
    "deer", "wild game", "pheasant", "no shell fish", "collard greens",
    "tilapia", "quail", "refrigerator", "canning", "moroccan",
    "pressure cooker", "squid", "korean", "plums", "danish", "creole",
    "mahi mahi", "tarts", "spinach", "hawaiian","homeopathy/remedies",
    "austrian",
    "thanksgiving",
    "moose",
    "bath/beauty",
    "swedish",
    "high fiber",
    "kosher",
    "norwegian",
    "household cleaner",
    "ethiopian",
    "belgian",
    "australian",
    "pennsylvania dutch",
    "bear",
    "scottish",
    "tempeh",
    "cuban",
    "turkey breasts",
    "cantonese",
    "tropical fruits",
    "peanut butter",
    "szechuan",
    "portuguese",
    "summer dip",
    "costa rican",
    "duck",
    "sweet",
    "nuts",
    "filipino",
    "welsh",
    "camping",
    "pot pie",
    "polynesian",
    "mango",
    "cherries",
    "egyptian",
    "chard",
    "lime",
    "lemon",
    "brunch",
    "toddler friendly",
    "kiwifruit",
    "whitefish",
    "south american",
    "malaysian",
    "octopus",
    "nigerian",
    "mixer",
    "venezuelan",
    "halloween",
    "stove top",
    "bread machine",
    "georgian",
    "south african",
    "finnish",
    "deep fried",
    "beginner cook",
    "steam",
    "small appliance",
    "nepalese",
    "palestinian",
    "egg free",
    "czech",
    "icelandic",
    "dairy free foods",
    "hunan",
    "avocado",
    "pakistani",
    "chocolate chip cookies",
    "chilean",
    "puerto rican",
    "ecuadorean",
    "oysters",
    "inexpensive",
    "hanukkah",
    "breakfast eggs",
    "cambodian",
    "honduran",
    "sudanese",
    "mongolian",
    "peruvian",
    "peanut butter pie",
    "ham and bean soup",
    "bread pudding",
    "fish tuna",
    "margarita",
    "bean soup",
    "turkey gravy",
    "spaghetti sauce",
    "freezer",
    "lemon cake",
    "buttermilk biscuits",
    "black bean soup",
    "gluten free appetizers",
    "somalian",
    "ice cream",
    "fish salmon",
    "snacks sweet",
    "main dish casseroles",
    "pot roast",
    "potato soup",
    "broccoli soup",
    "apple pie",
    "oatmeal",
    "soups crock pot",
    "roast beef crock pot",
    "from scratch",
    "artichoke",
    "key lime pie",
    "chicken crock pot",
    "wheat bread",
    "mushroom soup",
    "indian",
    "breakfast casseroles",
    "grapes",
    "macaroni and cheese",
    "mashed potatoes",
    "desserts fruit",
    "birthday",
    "pumpkin",
    "baking",
    "beef liver",
    "memorial day",
    "guatemalan",
    "coconut cream pie",
    "labor day"
]

def find_closest_category(category):
    """Find the closest matching category from the dataset."""
    if not category:
        return ""
    
    # First check for exact match
    if category.lower() in [c.lower() for c in RECIPE_CATEGORIES]:
        return next(c for c in RECIPE_CATEGORIES if c.lower() == category.lower())
    
    # For compound categories, check parts
    category_parts = category.lower().split()
    for part in category_parts:
        matches = [c for c in RECIPE_CATEGORIES if part in c.lower()]
        if matches:
            return matches[0]
    
    # If no matches found, use difflib to find closest match
    matches = get_close_matches(category.lower(), [c.lower() for c in RECIPE_CATEGORIES], n=1, cutoff=0.6)
    if matches:
        return next(c for c in RECIPE_CATEGORIES if c.lower() == matches[0])
    
    # If no match is found at all, return empty string
    return ""

def extract_recipe_attributes(text):
    messages = [
        {"role": "system", "content": "You are an assistant that extracts recipe attributes from user input."},
        {"role": "user", "content": f"""
From the given text, identify:
- **category**: The main name or type of the recipe (like "chicken soup"). 
- **calories**: Number of calories, if mentioned.
- **time**: Time to cook, in minutes.
- **keywords**: Important words related to the recipe. If the category is not common (like "noodles" or "biryani"), include relevant characteristics (e.g., "asian", "main course", "stir fry", "quick meal", "wheat based", "high protein", etc).
- **keywords_name**: List of individual words from the category/name. For uncommon categories, include descriptive terms and related categories (e.g., for "noodles": ["asian", "pasta", "wheat", "main dish"]).

Examples:
---
Input: "noodles"
Output: {{
    "category": "noodles",
    "calories": "",
    "time": "",
    "keywords": ["asian", "stir fry", "wheat based", "quick meal", "main course", "pasta"],
    "keywords_name": ["asian", "pasta", "main dish", "wheat"]
}}

---
Input: "biryani"
Output: {{
    "category": "biryani",
    "calories": "",
    "time": "",
    "keywords": ["rice", "indian", "spicy", "main course", "one dish meal"],
    "keywords_name": ["rice", "indian", "spicy"]
}}

---
Input: "sushi"
Output: {{
    "category": "sushi",
    "calories": "",
    "time": "",
    "keywords": ["japanese", "rice", "seafood", "raw fish", "snack", "main course"],
    "keywords_name": ["japanese", "seafood", "rice"]
}}

---
Input: "vegetable curry"
Output: {{
    "category": "vegetable curry",
    "calories": "",
    "time": "",
    "keywords": ["indian", "vegetarian", "spicy", "main course", "curry"],
    "keywords_name": ["indian", "vegetarian", "spicy"]
}}
         
---
Input: "quinoa salad"
Output: {{
    "category": "quinoa salad",
    "calories": "",
    "time": "",
    "keywords": ["healthy", "salad", "gluten-free", "fiber", "low calorie", "vegan"],
    "keywords_name": ["healthy", "salad", "vegan"]
}}

---
Input: "beef tacos"
Output: {{
    "category": "beef tacos",
    "calories": "",
    "time": "",
    "keywords": ["mexican", "beef", "spicy", "snack", "tortilla", "street food"],
    "keywords_name": ["mexican", "beef", "snack"]
}}

--- 
Input: "chocolate chip cookies"
Output: {{
    "category": "chocolate chip cookies",
    "calories": "",
    "time": "",
    "keywords": ["dessert", "baked", "chocolate", "sweet", "snack", "cookie"],
    "keywords_name": ["dessert", "chocolate", "snack"]
}}

---
Input: "caesar salad"
Output: {{
    "category": "caesar salad",
    "calories": "",
    "time": "",
    "keywords": ["salad", "appetizer", "healthy", "vegetables", "parmesan", "croutons"],
    "keywords_name": ["salad", "appetizer", "healthy"]
}}


---
Input: "smoothie bowl"
Output: {{
    "category": "smoothie bowl",
    "calories": "",
    "time": "",
    "keywords": ["breakfast", "healthy", "fruits", "smoothie", "vegan", "fiber"],
    "keywords_name": ["breakfast", "healthy", "fruits"]
}}

Input: "spaghetti bolognese"
Output: {{
    "category": "spaghetti bolognese",
    "calories": "",
    "time": "",
    "keywords": ["italian", "pasta", "meat", "tomato", "main course", "hearty"],
    "keywords_name": ["italian", "pasta", "meat"]
}}
         
---
Input: "I wish to cook chicken soup which contains around 200 calories within 30 mins"
Output: {{
    "category": "chicken soup",
    "calories": "200",
    "time": "30",
    "keywords": ["chicken", "soup", "200 calories", "30 mins"],
    "keywords_name": ["chicken", "soup"]
}}

---
Input: "Quick pasta recipe with 500 calories, ready in 20 mins"
Output: {{
    "category": "pasta",
    "calories": "500",
    "time": "20",
    "keywords": ["pasta", "500 calories", "20 mins"],
    "keywords_name": ["pasta"]
}}

---
Input: "uh i wish to cook something which contains protein"
Output: {{
    "category": "protein",
    "calories": "",
    "time": "",
    "keywords": ["protein"],
    "keywords_name": ["protein"]
}}

---
Input: "can you suggest something with low calories"
Output: {{
    "category": "low calories",
    "calories": "",
    "time": "",
    "keywords": ["low calories"],
    "keywords_name": ["low", "calories"]
}}

---
Input: "looking for a vegetarian recipe"
Output: {{
    "category": "vegetarian",
    "calories": "",
    "time": "",
    "keywords": ["vegetarian"],
    "keywords_name": ["vegetarian"]
}}

---
Input: "need something gluten free"
Output: {{
    "category": "gluten free",
    "calories": "",
    "time": "",
    "keywords": ["gluten free"],
    "keywords_name": ["gluten", "free"]
}}

---
Input: "want to make something dairy free"
Output: {{
    "category": "dairy free",
    "calories": "",
    "time": "",
    "keywords": ["dairy free"],
    "keywords_name": ["dairy", "free"]
}}

---
Input: "what can i cook for dinner"
Output: {{
    "category": "dinner",
    "calories": "",
    "time": "",
    "keywords": ["dinner"],
    "keywords_name": ["dinner"]
}}
         
---
Input: "something with low carbs"
Output: {{
    "category": "low carbs",
    "calories": "",
    "time": "",
    "keywords": ["low carbs"],
    "keywords_name": ["low", "carbs"]
}}
         
---
Input: "i wish to cook something in 30 minutes"
Output: {{
    "category": "",
    "calories": "",
    "time": "30",
    "keywords": ["30 minutes"],
    "keywords_name": [""]
}}

---
Input: "I wish to make fish and stew"
Output: {{
    "category": "fish",
    "calories": "",
    "time": "",
    "keywords": ["fish", "stew"],
    "keywords_name": ["fish", "stew"]
}}

---
Input: "give some recipes involving almonds or dry fruits"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["almonds", "dry fruits"],
    "keywords_name": ["almonds", "dry fruits"]
}}
           
---
Now process this input:
Input: "{text}"
Output:
"""}
    ]

    # Send the prompt to OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Process the response
    output_text = response['choices'][0]['message']['content'].strip()
    
    try:
        result = json.loads(output_text)
        # Update category with closest match from dataset
        original_category = result["category"]
        matched_category = find_closest_category(original_category)
        
        if matched_category:
            # If we found a match (exact or close), update category and keywords_name
            result["category"] = matched_category
            if original_category != matched_category:
                result["keywords_name"] = matched_category.split()
        else:
            # If no match found, empty the category but keep the GPT-generated
            # keywords and keywords_name as they should contain relevant features
            result["category"] = ""
            # Keep the existing keywords and keywords_name from GPT's response
            
    except json.JSONDecodeError:
        result = {"error": "Failed to parse JSON", "output": output_text}
    
    return result

# Example usage:
if __name__ == '__main__':
    test_cases = [
        # "noodles",
        # "need a pasta recipe",
        # "looking for a chicken dish",
        # "want to make something with rice",
        # "need a dessert recipe",
        # "biryani",
        # "30 mins",
        # "chole bhature",
        # "give some recipes involving almonds",
        "latte with foam, coffee, milk"
    ]
    
    for test_input in test_cases:
        print(f"\nTesting: {test_input}")
        result = extract_recipe_attributes(test_input)
        print(json.dumps(result, indent=2)) 