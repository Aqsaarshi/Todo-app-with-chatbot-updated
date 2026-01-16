from jose import jwt
import os
from uuid import UUID

# Test JWT decoding
SECRET_KEY = "mypassword123"  # Same as in the backend
ALGORITHM = "HS256"

# Sample token from our test
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMzI1ZmE0Yi1iNGZlLTQzYmQtYjVkYy0zMjJkMWVjZTViN2MiLCJlbWFpbCI6InRlc3R1c2VyMkBleGFtcGxlLmNvbSIsImV4cCI6MTc2ODQxOTAwN30.YGe4HKbVcbOaYioYLijuVR-P3U0CnAedG1ew1wnxKlc"

try:
    # Decode the token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Decoded payload: {payload}")

    user_id_from_token = payload.get("sub")
    print(f"User ID from token: {user_id_from_token}")

    # Try to convert to UUID (as done in the backend)
    user_id_uuid = UUID(user_id_from_token)
    print(f"Converted to UUID: {user_id_uuid}")

    # Test with the user ID from the logs
    user_id_from_logs = "8e92c421-274b-439c-9101-13da389a8e4b"
    user_id_logs_uuid = UUID(user_id_from_logs)
    print(f"User ID from logs as UUID: {user_id_logs_uuid}")

    # Compare
    print(f"Do they match? {user_id_uuid == user_id_logs_uuid}")

except Exception as e:
    print(f"Error decoding token: {e}")