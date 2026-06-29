# OrderTogether Backend API

Base URL (dev): `http://localhost:8080`

## POST `/api/match`

Find restaurants serving every diner's dish preference at once.

### Headers
| Header          | Required | Notes                                                          |
|-----------------|----------|----------------------------------------------------------------|
| `Content-Type`  | yes      | `application/json`                                              |
| `Authorization` | no\*     | `Bearer <oauth-access-token>`. Forwarded to the Swiggy MCP.    |

\* If omitted, the backend uses the `SWIGGY_MCP_TOKEN` env/property fallback (dev only).

### Request body
```json
{
  "preferences": ["shawarma", "dal tadka"],
  "addressId": "d3su1n0nfvanns8h7l4g"
}
```
- `preferences` — 1–10 dish terms, one per person. Blank/duplicate (case-insensitive) terms are ignored.
- `addressId` — optional; falls back to the server default when omitted.

### Response `200 OK`
```json
{
  "preferences": ["shawarma", "dal tadka"],
  "matchCount": 2,
  "restaurants": [
    {
      "id": "12345",
      "name": "Grill Inn",
      "avgRating": 4.8,
      "deliveryTimeMinutes": 25,
      "costForTwo": "₹300 for two",
      "availabilityStatus": "OPEN",
      "imageUrl": "https://.../img.jpg",
      "cuisines": ["North Indian", "Arabian"],
      "matchedPreferences": ["shawarma", "dal tadka"],
      "appDeepLink": "swiggy://menu?restaurant_id=12345",
      "webUrl": "https://www.swiggy.com/restaurants/12345"
    }
  ]
}
```
Restaurants are ranked best-first: `avgRating` desc, then `deliveryTimeMinutes` asc.
CLOSED restaurants are excluded. An empty `restaurants` array means no single restaurant
serves all preferences.

> **Note:** `appDeepLink` uses a best-effort `swiggy://` scheme — confirm the exact
> format during Swiggy app integration; `webUrl` is the reliable fallback.

### Errors (RFC 7807 `application/problem+json`)
- `400 Bad Request` — validation failed (e.g. empty `preferences`).
- `502 Bad Gateway` — upstream Swiggy MCP call failed.
