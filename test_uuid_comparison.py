from uuid import UUID

# Simulate the scenario
user_id_from_token = "dc9f498e-b24f-43d3-aff5-4398d90a4140"
path_user_id = "dc9f498e-b24f-43d3-aff5-4398d90a4140"

# Convert token user ID to UUID (as done in get_current_user)
try:
    uuid_from_token = UUID(user_id_from_token)
    print(f"UUID from token: {uuid_from_token} (type: {type(uuid_from_token)})")
except ValueError:
    uuid_from_token = user_id_from_token
    print(f"String from token: {uuid_from_token} (type: {type(uuid_from_token)})")

print(f"Path user ID: {path_user_id} (type: {type(path_user_id)})")

# Check equality
print(f"Are they equal? {uuid_from_token == path_user_id}")
print(f"String representation equal? {str(uuid_from_token) == path_user_id}")