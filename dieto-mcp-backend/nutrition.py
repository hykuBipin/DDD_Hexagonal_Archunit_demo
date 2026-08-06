# Local nutritional database mapping shared Swiggy dishes to caloric profiles
NUTRITION_DATABASE = {
    "shawarma": {
        "name": "Shawarma",
        "calories": 550,
        "carbs": 42.0,
        "protein": 24.0,
        "fat": 28.0,
        "is_estimated": False
    },
    "dal tadka": {
        "name": "Dal Tadka",
        "calories": 450,
        "carbs": 58.0,
        "protein": 18.0,
        "fat": 12.0,
        "is_estimated": False
    },
    "chicken tikka wrap": {
        "name": "Chicken Tikka Wrap",
        "calories": 480,
        "carbs": 38.0,
        "protein": 32.0,
        "fat": 15.0,
        "is_estimated": False
    },
    "egg biryani": {
        "name": "Egg Biryani",
        "calories": 590,
        "carbs": 68.0,
        "protein": 24.0,
        "fat": 18.0,
        "is_estimated": False
    },
    "paneer rice bowl": {
        "name": "Paneer Rice Bowl",
        "calories": 560,
        "carbs": 65.0,
        "protein": 20.0,
        "fat": 22.0,
        "is_estimated": False
    },
    "double cheese burger": {
        "name": "Double Cheese Burger",
        "calories": 680,
        "carbs": 42.0,
        "protein": 28.0,
        "fat": 36.0,
        "is_estimated": False
    },
    "tandoori chicken salad": {
        "name": "Tandoori Chicken Salad",
        "calories": 350,
        "carbs": 12.0,
        "protein": 35.0,
        "fat": 10.0,
        "is_estimated": False
    },
    "butter chicken & naan": {
        "name": "Butter Chicken & Naan",
        "calories": 850,
        "carbs": 85.0,
        "protein": 38.0,
        "fat": 42.0,
        "is_estimated": False
    },
    "lime soda": {
        "name": "Lime Soda",
        "calories": 120,
        "carbs": 30.0,
        "protein": 0.0,
        "fat": 0.0,
        "is_estimated": False
    },
    "mint juice": {
        "name": "Mint Juice (Detox)",
        "calories": 45,
        "carbs": 10.0,
        "protein": 1.0,
        "fat": 0.0,
        "is_estimated": False
    },
    "raita": {
        "name": "Raita",
        "calories": 80,
        "carbs": 6.0,
        "protein": 3.0,
        "fat": 4.0,
        "is_estimated": False
    }
}

def estimate_nutrition(dish_name: str) -> dict:
    """
    Looks up dish nutrition statistics exactly, falling back to heuristics based on keywords.
    """
    clean_name = dish_name.lower().strip()
    if clean_name in NUTRITION_DATABASE:
        return NUTRITION_DATABASE[clean_name]
        
    # Heuristic fallback matching
    if "biryani" in clean_name:
        if "egg" in clean_name:
            return {**NUTRITION_DATABASE["egg biryani"], "name": dish_name, "is_estimated": True}
        return {
            "name": dish_name,
            "calories": 650,
            "carbs": 70.0,
            "protein": 28.0,
            "fat": 20.0,
            "is_estimated": True
        }
        
    if "shawarma" in clean_name:
        return {**NUTRITION_DATABASE["shawarma"], "name": dish_name, "is_estimated": True}
        
    if "dal" in clean_name:
        return {**NUTRITION_DATABASE["dal tadka"], "name": dish_name, "is_estimated": True}

    if "salad" in clean_name:
        return {**NUTRITION_DATABASE["tandoori chicken salad"], "name": dish_name, "is_estimated": True}

    if "wrap" in clean_name or "roll" in clean_name:
        return {**NUTRITION_DATABASE["chicken tikka wrap"], "name": dish_name, "is_estimated": True}

    if "burger" in clean_name:
        return {**NUTRITION_DATABASE["double cheese burger"], "name": dish_name, "is_estimated": True}

    if "soda" in clean_name or "coke" in clean_name:
        return {**NUTRITION_DATABASE["lime soda"], "name": dish_name, "is_estimated": True}

    if "juice" in clean_name or "detox" in clean_name:
        return {**NUTRITION_DATABASE["mint juice"], "name": dish_name, "is_estimated": True}

    # General default fallback
    return {
        "name": dish_name,
        "calories": 450,
        "carbs": 45.0,
        "protein": 15.0,
        "fat": 15.0,
        "is_estimated": True
    }
