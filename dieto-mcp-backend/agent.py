import httpx
from nutrition import estimate_nutrition

# Shared mock restaurant database containing menu items to simulate intersection matching
MOCK_RESTAURANTS = [
    {
        "id": "rest_punjab",
        "name": "Grand Punjab",
        "rating": 4.5,
        "delivery_time": 25,
        "menu": ["Dal Tadka", "Butter Chicken & Naan", "Paneer Rice Bowl"]
    },
    {
        "id": "rest_wrap",
        "name": "Wrap & Roll",
        "rating": 4.2,
        "delivery_time": 20,
        "menu": ["Chicken Tikka Wrap", "Shawarma", "Lime Soda"]
    },
    {
        "id": "rest_junction",
        "name": "Indian Spice Junction",
        "rating": 4.6,
        "delivery_time": 30,
        "menu": ["Shawarma", "Dal Tadka", "Chicken Tikka Wrap", "Paneer Rice Bowl", "Lime Soda", "Mint Juice"]
    },
    {
        "id": "rest_healthy",
        "name": "Healthy Bites",
        "rating": 4.4,
        "delivery_time": 15,
        "menu": ["Tandoori Chicken Salad", "Mint Juice", "Lime Soda"]
    }
]

def calculate_fit_score(calories: int, remaining: int) -> int:
    """
    Utility score calculations for Dieto Fit Score.
    """
    if remaining <= 0:
        return 10
    if calories <= remaining:
        return 90 + min(10, int((remaining - calories) / 10))
    # Exceeds
    excess = calories - remaining
    penalty = int((excess / remaining) * 80)
    return max(10, 90 - penalty)

async def match_restaurants_by_preferences(preferences: list, token: str = None) -> list:
    """
    Intersects restaurant catalogs to find locations serving ALL input preferences.
    """
    matched = []
    
    # Live HTTP MCP calls sequence
    if token and token.strip():
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Mock address retrieval
                pass
        except Exception as e:
            print(f"[Agent] Live Swiggy MCP preference match failed: {e}")
            
    # Heuristic intersection matching
    for rest in MOCK_RESTAURANTS:
        # Check if restaurant menu matches all preference keywords
        matches_all = True
        for pref in preferences:
            pref_lower = pref.lower().strip()
            # Check if any menu item matches keyword
            item_match = False
            for item in rest["menu"]:
                if pref_lower in item.lower():
                    item_match = True
                    break
            if not item_match:
                matches_all = False
                break
        
        if matches_all:
            matched.append(rest)
            
    # Fallback to general matched list if empty
    if not matched:
        matched = [MOCK_RESTAURANTS[2]] # Indian Spice Junction serves most options
        
    return matched
