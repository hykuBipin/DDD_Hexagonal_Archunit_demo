# OrderTogether

Finds restaurants on Swiggy that satisfy **multiple people's dish preferences at once**
(e.g. person 1 wants shawarma, person 2 wants dal tadka → restaurants serving both).

MVP is **discovery only**: show matched restaurants and deep-link into the Swiggy app to
complete the order. No in-app ordering in v1.

## Repo layout

| Directory                  | Stack         | Purpose                                              |
|----------------------------|---------------|------------------------------------------------------|
| `order-together-backend/`  | Spring Boot 3 | Calls the Swiggy MCP, intersects & ranks restaurants |
| `frontend/`                | Flutter       | Android-first UI (to be scaffolded)                  |

## Backend quick start

```bash
cd order-together-backend
# Optional: provide a dev token instead of forwarding one per request
export SWIGGY_MCP_TOKEN=<oauth-access-token>
./mvnw spring-boot:run
```

Then:

```bash
curl -s http://localhost:8080/api/match \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <oauth-access-token>' \
  -d '{"preferences":["shawarma","dal tadka"],"addressId":"d3su1n0nfvanns8h7l4g"}'
```

See [`order-together-backend/API.md`](order-together-backend/API.md) for the full request/response contract that the
Flutter client codes against.

## How matching works

1. Fan out one `search_restaurants` MCP call **per preference**, in parallel.
2. **Intersect** restaurant ids that appear in *every* preference's results.
3. Drop anything with `availabilityStatus == "CLOSED"`.
4. **Rank** by `avgRating` (desc), then `deliveryTimeMinutes` (asc).

## Auth

OAuth 2.1 with PKCE against `https://mcp.swiggy.com`. The Flutter client performs the
auth flow and forwards the bearer token to the backend, which relays it to the MCP server.
For local dev the backend can fall back to `SWIGGY_MCP_TOKEN`.

Brand colors: orange `#FC8019`, white, dark grey.
