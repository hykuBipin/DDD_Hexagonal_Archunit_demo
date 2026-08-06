from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import agent
import nutrition
import wellness
import ui

app = FastAPI(
    title="OrderTogether Dieto Caretaker API",
    description="Backend engine mapping shared Swiggy MCP matching to Dieto AI wellness suggestions."
)

# ----------------- Schemas -----------------

class MatchPreferencesRequest(BaseModel):
    preferences: List[str]
    token: Optional[str] = None

class SyncOrderRequest(BaseModel):
    order_id: str
    token: Optional[str] = None

class ComparePlateRequest(BaseModel):
    order_id: str
    detected_items: List[str]
    no_sugar: Optional[bool] = False
    no_garlic: Optional[bool] = False
    gluten_free: Optional[bool] = False

class RecoveryRequest(BaseModel):
    excess_calories: int
    no_sugar: Optional[bool] = False
    no_garlic: Optional[bool] = False
    gluten_free: Optional[bool] = False
    cart_items: Optional[List[str]] = []

# ----------------- Mock Swiggy Orders -----------------
MOCK_SWIGGY_ORDERS = {
    "ord_swiggy_7711": ["Chicken Biryani", "Chicken 65", "Lime Soda"],
    "ord_swiggy_8822": ["Paneer Tikka Roll", "Lime Soda"],
    "ord_swiggy_9933": ["Tandoori Chicken Salad"]
}

# ----------------- Endpoints -----------------

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """
    Serves the group order calorimeter caretaker dashboard.
    """
    return ui.HTML_CONTENT

@app.post("/match")
async def match_restaurants(req: MatchPreferencesRequest):
    """
    Finds restaurants satisfying joint dining preferences.
    """
    try:
        results = await agent.match_restaurants_by_preferences(
            preferences=req.preferences,
            token=req.token
        )
        return {
            "preferences": req.preferences,
            "matched_restaurants": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync-order")
async def sync_order(req: SyncOrderRequest):
    """
    Calorimeter sync. Maps ordered items to estimated nutrition.
    """
    order_id = req.order_id
    items = MOCK_SWIGGY_ORDERS.get(order_id, ["Chicken Biryani"])
    
    total_calories = 0
    total_carbs = 0.0
    total_protein = 0.0
    total_fat = 0.0
    mapped_items = []

    for item in items:
        nut = nutrition.estimate_nutrition(item)
        total_calories += nut["calories"]
        total_carbs += nut["carbs"]
        total_protein += nut["protein"]
        total_fat += nut["fat"]
        mapped_items.append(nut)

    return {
        "order_id": order_id,
        "items": items,
        "total_calories": total_calories,
        "total_protein": total_protein,
        "mapped_nutrition": mapped_items
    }

@app.post("/compare-plate")
async def compare_plate(req: ComparePlateRequest):
    """
    Portion comparison scanner.
    """
    order_items = MOCK_SWIGGY_ORDERS.get(req.order_id, ["Chicken Biryani"])
    order_calories = sum(nutrition.estimate_nutrition(i)["calories"] for i in order_items)
    
    plate_calories = sum(nutrition.estimate_nutrition(i)["calories"] for i in req.detected_items)
    
    diff = plate_calories - order_calories
    
    message = "Your plate matches your order perfectly!"
    if diff > 0:
        message = f"Divergence found: actual plate has +{diff} kcal excess."
    elif diff < 0:
        message = f"You ate lighter by -{abs(diff)} kcal!"
        
    coach_advice = wellness.get_recovery_advice(
        diff if diff > 0 else 0,
        no_sugar=req.no_sugar,
        no_garlic=req.no_garlic,
        gluten_free=req.gluten_free,
        cart_items=req.detected_items
    )
    
    return {
        "order_id": req.order_id,
        "order_estimated_calories": order_calories,
        "plate_scanned_calories": plate_calories,
        "calorie_difference": diff,
        "comparison_result": message,
        "coach_advice": coach_advice
    }

@app.post("/recovery")
async def get_recovery(req: RecoveryRequest):
    """
    Exposes recovery coach.
    """
    return wellness.get_recovery_advice(
        req.excess_calories,
        no_sugar=req.no_sugar,
        no_garlic=req.no_garlic,
        gluten_free=req.gluten_free,
        cart_items=req.cart_items
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
