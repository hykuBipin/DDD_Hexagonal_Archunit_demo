from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def run_tests():
    print("==================================================")
    print("   AI-DIETO-UPDATED GROUP BACKEND VERIFIER")
    print("==================================================\n")

    # Test 1: POST /match
    print("--- Test 1: Matching Diner Preferences ---")
    match_payload = {
        "preferences": ["shawarma", "dal tadka"]
    }
    resp = client.post("/match", json=match_payload)
    print(f"Status: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2))
    print("\n")

    # Test 2: POST /sync-order
    print("--- Test 2: Sync Order ---")
    sync_payload = {
        "order_id": "ord_swiggy_7711"
    }
    resp = client.post("/sync-order", json=sync_payload)
    print(f"Status: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2))
    print("\n")

    # Test 3: POST /compare-plate
    print("--- Test 3: Plate Scan Comparison ---")
    compare_payload = {
        "order_id": "ord_swiggy_7711",
        "detected_items": ["Chicken Biryani", "Chicken 65", "Raita"]
    }
    resp = client.post("/compare-plate", json=compare_payload)
    print(f"Status: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2))
    print("\n")

if __name__ == "__main__":
    run_tests()
