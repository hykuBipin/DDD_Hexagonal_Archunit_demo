# AI-Dieto-Updated

**AI-Dieto-Updated** is a health-conscious group food ordering companion powered by the **Swiggy MCP Food Server** (`mcp.swiggy.com/food`). It helps groups of diners find shared restaurant options, estimate calorie intake, and receive caretaker tips and post-meal recovery suggestions to keep dining flexible and balanced.

---

## 🚀 Key Features

1. **Preference Intersection Matching**:
   * Takes preferences from multiple diners (e.g. Diner 1 wants "shawarma", Diner 2 wants "dal tadka").
   * Calls Swiggy MCP `search_restaurants` to find locations that satisfy all dietary preferences in a single order.

2. **Diner Calorie Tracker Dashboard**:
   * Tracks individual budget targets (Strict: 1,600 kcal, Balanced: 2,000 kcal, Relaxed: 2,800 kcal).
   * Displays joint progress bars for all diners in the group.

3. **Caretaker Wellness Tips**:
   * If a diner's chosen dish exceeds their daily budget, the Caretaker engine recommends:
     * **Neutralizing Menu Swaps**: (e.g., Swap Shawarma for Wheat Wrap to save 130 kcal).
     * **Detox Boosters**: (e.g., Add Lime Mint Juice).
     * **Digestion Walks**: (e.g., A 15-20 min light walk post-meal).

4. **MCP Checkout Logs**:
   * Simulates clean sequential tool outputs on checkout:
     * `[MCP] Call: get_addresses() -> Completed (200 OK)`
     * `[MCP] Call: update_food_cart() -> Completed (200 OK)`
     * `[MCP] Call: place_food_order() -> Completed (200 OK)`

5. **Post-Order Plate Scanner**:
   * Captures photos of delivered plates, computes portional calorie differences, and outputs recovery advice.

---

## 📂 Repository Layout

| Directory | Stack | Purpose |
|---|---|---|
| `dieto-mcp-backend/` | FastAPI, Pydantic, Python | The Calorimeter service, database, and caretaker UI dashboard. |
| `order-together-backend/` | Spring Boot 3 | Java backend performing live preference matching. |
| `frontend/` | Flutter | Android/iOS client template for Order Together. |

---

## ⚡ Quick Start

### Start the Dieto Calorimeter Dashboard

1. Navigate to the backend directory:
   ```bash
   cd dieto-mcp-backend
   ```
2. Activate virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the FastAPI application:
   ```bash
   python3 main.py
   ```
4. Open your browser and navigate to:
   👉 **`http://localhost:8000/`**

---

## 🧪 Running Verifications

To verify backend endpoints and nutrition mapping:
```bash
python3 verify.py
```
