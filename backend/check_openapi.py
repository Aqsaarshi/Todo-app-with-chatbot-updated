from src.main import app
import json

# Get the OpenAPI schema
openapi_schema = app.openapi()

# Write it to a file for inspection
with open("openapi_schema.json", "w") as f:
    json.dump(openapi_schema, f, indent=2)

print("OpenAPI schema written to openapi_schema.json")
print("Checking for chat paths in the schema...")

paths = openapi_schema.get("paths", {})
chat_paths = {path: details for path, details in paths.items() if "chat" in path or "conversation" in path}

print(f"Found {len(chat_paths)} chat/conversation paths:")
for path, details in chat_paths.items():
    print(f"  {path}: {list(details.keys())}")