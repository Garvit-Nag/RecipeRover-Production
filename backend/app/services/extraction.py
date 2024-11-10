import openai
import json
from difflib import get_close_matches
import os
from dotenv import load_dotenv
from difflib import SequenceMatcher

load_dotenv() 
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define categories from dataset
RECIPE_CATEGORIES = [
    "frozen desserts",
    "chicken breast",
    "beverages",
    "soy/tofu",
    "vegetable",
    "pie",
    "chicken",
    "dessert",
    "southwestern u.s.",
    "sauces",
    "stew",
    "black beans",
    "< 60 mins",
    "lactose free",
    "yeast breads",
    "whole chicken",
    "cheesecake",
    "free of...",
    "brazilian",
    "breakfast",
    "breads",
    "bar cookie",
    "brown rice",
    "oranges",
    "pork",
    "low protein",
    "asian",
    "potato",
    "cheese",
    "halibut",
    "meat",
    "lamb/sheep",
    "very low carbs",
    "spaghetti",
    "scones",
    "drop cookies",
    "lunch/snacks",
    "beans",
    "punch beverage",
    "pineapple",
    "quick breads",
    "sourdough breads",
    "curries",
    "chicken livers",
    "coconut",
    "savory pies",
    "poultry",
    "steak",
    "healthy",
    "rice",
    "apple",
    "spreads",
    "crab",
    "jellies",
    "pears",
    "chowders",
    "cauliflower",
    "candy",
    "chutneys",
    "white rice",
    "tex mex",
    "bass",
    "fruit",
    "european",
    "smoothies",
    "manicotti",
    "onions",
    "new zealand",
    "chicken thigh & leg",
    "indonesian",
    "greek",
    "corn",
    "lentil",
    "long grain rice",
    "southwest asia (middle east)",
    "spanish",
    "dutch",
    "gelatin",
    "tuna",
    "citrus",
    "berries",
    "peppers",
    "salad dressings",
    "clear soup",
    "mexican",
    "raspberries",
    "crawfish",
    "beef organ meats",
    "lobster",
    "strawberry",
    "shakes",
    "short grain rice",
    "< 15 mins",
    "german",
    "one dish meal",
    "thai",
    "cajun",
    "russian",
    "melons",
    "swiss",
    "papaya",
    "veal",
    "orange roughy",
    "canadian",
    "caribbean",
    "mussels",
    "medium grain rice",
    "japanese",
    "penne",
    "elk",
    "colombian",
    "gumbo",
    "roast beef",
    "perch",
    "vietnamese",
    "rabbit",
    "lebanese",
    "turkish",
    "kid friendly",
    "whole turkey",
    "chinese",
    "grains",
    "yam/sweet potato",
    "meatloaf",
    "trout",
    "african",
    "ham",
    "goose",
    "pasta shells",
    "stocks",
    "meatballs",
    "whole duck",
    "scandinavian",
    "greens",
    "catfish",
    "duck breasts",
    "polish",
    "deer",
    "wild game",
    "pheasant",
    "hungarian",
    "no shell fish",
    "collard greens",
    "tilapia",
    "quail",
    "moroccan",
    "squid",
    "korean",
    "plums",
    "danish",
    "creole",
    "mahi mahi",
    "tarts",
    "hawaiian",
    "austrian",
    "moose",
    "native american",
    "swedish",
    "norwegian",
    "ethiopian",
    "belgian",
    "australian",
    "bear",
    "scottish",
    "tempeh",
    "cuban",
    "spinach",
    "turkey breasts",
    "cantonese",
    "tropical fruits",
    "peanut butter",
    "szechuan",
    "portuguese",
    "costa rican",
    "duck",
    "nuts",
    "filipino",
    "pot pie",
    "polynesian",
    "mango",
    "cherries",
    "egyptian",
    "chard",
    "lime",
    "lemon",
    "kiwifruit",
    "whitefish",
    "south american",
    "malaysian",
    "octopus",
    "nigerian",
    "south african",
    "nepalese",
    "palestinian",
    "czech",
    "avocado",
    "iraqi",
    "pakistani",
    "chocolate chip cookies",
    "finnish",
    "puerto rican",
    "cambodian",
    "honduran",
    "mongolian",
    "peruvian",
    "turkey gravy",
    "somalian",
    "ice cream",
    "oatmeal",
    "artichoke",
    "indian",
    "grapes",
    "macaroni and cheese",
    "mashed potatoes",
    "pumpkin",
    "guatemalan"
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
    if len(category_parts) == 1 and category_parts[0] in [c.lower() for c in RECIPE_CATEGORIES]:
        # If the input is a single word that exists in the category list, return it
        return next(c for c in RECIPE_CATEGORIES if c.lower() == category_parts[0])
    
    for part in category_parts:
        matches = [c for c in RECIPE_CATEGORIES if part in c.lower()]
        if matches:
            return matches[0]
    
    # If no matches found, use difflib to find closest match
    matches = get_close_matches(category.lower(), [c.lower() for c in RECIPE_CATEGORIES], n=1, cutoff=0.75)
    if matches:
        closest_match = matches[0]
        # Check if the closest match is close enough (similarity score > 0.8)
        if SequenceMatcher(None, category.lower(), closest_match).ratio() > 0.8:
            return next(c for c in RECIPE_CATEGORIES if c.lower() == closest_match)
        else:
            return ""
    
    # If no match is found at all, return empty string
    return ""

def extract_recipe_attributes(text):
    messages = [
        {"role": "system", "content": "You are an assistant that extracts recipe attributes from user input. If the input contains an uncommon or unrecognized category, add relevant general keywords based on common culinary types, such as 'beverages' for drinks, 'dessert' for sweets, etc."},
        {"role": "user", "content": f"""
From the given text, identify:
- **category**: The main name or type of the recipe (like "chicken", "ice cream"). 
- **calories**: Number of calories, if mentioned.
- **time**: Time to cook, in minutes.
- **keywords**: Important words related to the recipe. If the category is not common (like "noodles" or "biryani"), include relevant characteristics (e.g., "asian", "main course", "stir fry", "quick meal", "wheat based", "high protein", etc).
- **keywords_name**: List of individual words from the category/name. For uncommon categories, include descriptive terms and related categories (e.g., for "noodles": ["asian", "pasta", "wheat", "main dish"]).

Examples:
---
Input: "noodles"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["asian", "stir fry", "wheat based", "quick meal", "main course", "pasta", "noodles"],
    "keywords_name": ["asian", "pasta", "main dish", "wheat"]
}}

---
Input: "biryani"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["rice", "indian", "spicy", "main course", "one dish meal", "biryani"],
    "keywords_name": ["rice", "indian", "spicy"]
}}

---
Input: "sushi"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["japanese", "rice", "seafood", "whitefish", "snack", "main course", "sushi"],
    "keywords_name": ["japanese", "seafood", "rice"]
}}

---
Input: "vegetable curry"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["vegan", "vegetarian", "spicy", "main course", "curry", "indian"],
    "keywords_name": ["indian", "vegetarian", "spicy"]
}}
         
---
Input: "quinoa salad"
Output: {{
    "category": "salad dressings",
    "calories": "",
    "time": "",
    "keywords": ["healthy", "salad", "gluten-free", "fiber", "low calorie", "vegan"],
    "keywords_name": ["healthy", "salad", "vegan"]
}}

---
Input: "beef tacos"
Output: {{
    "category": "beef organ meats",
    "calories": "",
    "time": "",
    "keywords": ["mexican", "beef", "spicy", "snack", "tortilla", "street food"],
    "keywords_name": ["mexican", "beef", "snack"]
}}

---
Input: "caesar salad"
Output: {{
    "category": "salad dressings",
    "calories": "",
    "time": "",
    "keywords": ["salad", "appetizer", "healthy", "vegetables", "parmesan", "croutons"],
    "keywords_name": ["salad", "appetizer", "healthy"]
}}


---
Input: "smoothie bowl"
Output: {{
    "category": "smoothies",
    "calories": "",
    "time": "",
    "keywords": ["breakfast", "healthy", "fruits", "smoothies", "vegan", "fiber"],
    "keywords_name": ["breakfast", "healthy", "fruits"]
}}

Input: "spaghetti bolognese"
Output: {{
    "category": "spaghetti",
    "calories": "",
    "time": "",
    "keywords": ["italian", "pasta", "meat", "tomato", "main course", "hearty"],
    "keywords_name": ["italian", "pasta", "meat"]
}}
         
---
Input: "I wish to cook chicken soup which contains around 200 calories within 30 mins"
Output: {{
    "category": "chicken",
    "calories": "200",
    "time": "30",
    "keywords": ["chicken", "soup", "200 calories", "30 mins"],
    "keywords_name": ["chicken", "soup"]
}}

---
Input: "Quick pasta recipe with 500 calories, ready in 20 mins"
Output: {{
    "category": "pasta shells",
    "calories": "500",
    "time": "20",
    "keywords": ["pasta shells", "500 calories", "20 mins"],
    "keywords_name": ["pasta shells"]
}}

---
Input: "uh i wish to cook something which contains protein"
Output: {{
    "category": "low protein",
    "calories": "",
    "time": "",
    "keywords": ["low protein", "high protein", "protein"],
    "keywords_name": ["low protein"]
}}

---
Input: "can you suggest something with low calories"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["low calories"],
    "keywords_name": ["low", "calories"]
}}

---
Input: "looking for a vegetarian recipe"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["vegetarian", "vegan"],
    "keywords_name": ["vegetarian"]
}}

---
Input: "need something gluten free"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["gluten free"],
    "keywords_name": ["gluten", "free"]
}}

---
Input: "want to make something dairy free"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["dairy free", "vegan"],
    "keywords_name": ["dairy", "free"]
}}

---
Input: "what can i cook for dinner"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["dinner", "vegan"],
    "keywords_name": [""]
}}

---
Input: "what can i cook for breakfast"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["breakfast", "vegan"],
    "keywords_name": [""]
}}

---
Input: "what can i cook for lunch"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["lunch", "quick meal", "vegan"],
    "keywords_name": [""]
}}
         
---
Input: "something with low carbs"
Output: {{
    "category": "very low carbs",
    "calories": "",
    "time": "",
    "keywords": ["very low carbs", "low carbs", "carbs"],
    "keywords_name": ["low", "carbs"]
}}
         
---
Input: "i wish to cook something in 30 minutes"
Output: {{
    "category": "",
    "calories": "",
    "time": "30",
    "keywords": ["30 minutes", "quick meal"],
    "keywords_name": [""]
}}

---
Input: "I wish to make fish and stew"
Output: {{
    "category": "stew",
    "calories": "",
    "time": "",
    "keywords": ["fish", "stew", "high protein"],
    "keywords_name": ["fish", "stew"]
}}

---
Input: "I wish to make fish and stew"
Output: {{
    "category": "catfish",
    "calories": "",
    "time": "",
    "keywords": ["fish", "stew", "high protein"],
    "keywords_name": ["fish", "stew"]
}}

---
Input: "I wish to make fish and stew"
Output: {{
    "category": "whitefish",
    "calories": "",
    "time": "",
    "keywords": ["fish", "stew", "high protein"],
    "keywords_name": ["fish", "stew"]
}}

---
Input: "I wish to make fish and stew"
Output: {{
    "category": "crawfish",
    "calories": "",
    "time": "",
    "keywords": ["fish", "stew", "high protein"],
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
Input: "tea with milk, sugar, water"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["milk", "sugar", "water", "beverages"],
    "keywords_name": [""]
}}

---
Input: "chole bhature"
Output: {{
    "category": "",
    "calories": "",
    "time": "",
    "keywords": ["gluten free"],
    "keywords_name": ["gluten", "free"]
}}

---
Input: "something involving nuts"
Output: {{
    "category": "nuts",
    "calories": "",
    "time": "",
    "keywords": ["nuts", "snack", "healthy", "protein", "fiber"],
    "keywords_name": ["nuts", "snack", "healthy"]
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
            result["category"] = ""
            # Add additional context-based keywords if category is empty
            if "coffee" in text.lower() or "latte" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["coffee", "beverages", "caffeinated", "hot drink"]
                result["keywords_name"] = result.get("keywords_name", []) + ["beverages", "caffeinated", "coffee"]
            elif "espresso" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["beverages", "caffeinated", "espresso"]
                result["keywords_name"] = result.get("keywords_name", []) + ["beverages", "espresso"]
            elif "smoothie bowl" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["beverages", "healthy", "smoothie bowl"]
                result["keywords_name"] = result.get("keywords_name", []) + ["beverages", "smoothie bowl"]
            elif "kombucha" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["beverage", "fermented", "kombucha"]
                result["keywords_name"] = result.get("keywords_name", []) + ["beverages", "kombucha"]
            elif "herbal tea" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["beverages", "caffeine-free", "herbal tea"]
                result["keywords_name"] = result.get("keywords_name", []) + ["beverages", "herbal tea"]
            elif "seaweed" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["ingredient", "seafood", "seaweed"]
                result["keywords_name"] = result.get("keywords_name", []) + ["seaweed"]
            elif "vegan cheese" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["dairy-free", "vegan", "cheese"]
                result["keywords_name"] = result.get("keywords_name", []) + ["vegan cheese"]
            elif "air fryer" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["cooking method", "air fryer", "healthy"]
                result["keywords_name"] = result.get("keywords_name", []) + ["air fryer"]
            elif "instant pot" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["cooking method", "instant pot", "pressure cooker"]
                result["keywords_name"] = result.get("keywords_name", []) + ["instant pot"]
            elif "sous vide" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["cooking method", "sous vide", "precision cooking"]
                result["keywords_name"] = result.get("keywords_name", []) + ["sous vide"]
            elif "paleo" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["diet", "paleo", "low-carb"]
                result["keywords_name"] = result.get("keywords_name", []) + ["paleo"]
            elif "fodmap" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["diet", "fodmap", "digestive health"]
                result["keywords_name"] = result.get("keywords_name", []) + ["fodmap"]
            elif "cold brew" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["beverages", "caffeinated", "cold coffee"]
                result["keywords_name"] = result.get("keywords_name", []) + ["beverages", "cold brew"]
            elif "matcha" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["beverages", "green tea", "matcha"]
                result["keywords_name"] = result.get("keywords_name", []) + ["beverages", "matcha"]
            elif "smoothie" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["beverages", "healthy", "smoothie"]
                result["keywords_name"] = result.get("keywords_name", []) + ["beverages", "smoothie"]
            elif "protein shake" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["beverages", "high protein", "shake"]
                result["keywords_name"] = result.get("keywords_name", []) + ["beverages", "protein shake"]
            elif "oat milk" in text.lower() or "almond milk" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["dairy-free", "vegan", "plant-based milk"]
                result["keywords_name"] = result.get("keywords_name", []) + ["oat milk" if "oat" in text.lower() else "almond milk"]
            elif "zoodles" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["low carb", "gluten-free", "vegetable noodles", "noodles"]
                result["keywords_name"] = result.get("keywords_name", []) + ["zoodles", "noodles"]
            elif "avocado toast" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["breakfast", "healthy", "avocado"]
                result["keywords_name"] = result.get("keywords_name", []) + ["avocado toast"]
            elif "golden milk" in text.lower():
                result["keywords"] = result.get("keywords", []) + ["beverage", "turmeric", "anti-inflammatory"]
                result["keywords_name"] = result.get("keywords_name", []) + ["golden milk"]
            # Add other cases as needed
            
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
        # "latte with foam, coffee, milk",
        # "cold drink beverage",
        # "beans",
        # "coffee",
        # "latte",
        # "something involving nuts",
        # "i wish to cook something with crab",
        # "livers",
        # "popcorn",
        # "beef stew with potatoes, carrots, and herbs.",
        # "dessert with chocolate, brownie, cake"
        # "chocolate, brownie, cake, brown sugar",
        # "avocado smoothie, avocado, milk, ice",
        # "momo, momo, sauce",
        # "I have basil, tomato and clove what can i make in 30 minutes",
        "basil"
    ]
    
    for test_input in test_cases:
        print(f"\nTesting: {test_input}")
        result = extract_recipe_attributes(test_input)
        print(json.dumps(result, indent=2)) 