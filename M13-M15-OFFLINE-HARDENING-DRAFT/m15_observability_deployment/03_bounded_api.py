"""M15: inspect the API contract before starting the local server."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bounded_api import app

routes = [route.path for route in app.routes]
assert "/health" in routes and "/v1/advisor/explain" in routes
print({"routes": routes, "boundary": "read-only, validated, local-model failure becomes 503"})
