from jose import jwt, JWTError
from uuid import UUID
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Your token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkYzlmNDk4ZS1iMjRmLTQzZDMtYWZmNS00Mzk4ZDkwYTQxNDAiLCJlbWFpbCI6ImFxc2FhcnNoaTVAZ21haWwuY29tIiwiZXhwIjoxNzY4NTU2NDgyfQ.G0EMyQPykV9uliKd-xcHLWlriSMsZ0gPI9Z5-ntGqZA"

try:
    # Decode the token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("Token payload:", payload)

    # Extract user ID from token
    user_id_from_token = payload.get("sub")
    print("User ID from token:", user_id_from_token)
    print("Type of user ID from token:", type(user_id_from_token))

    # Try to convert to UUID
    try:
        uuid_from_token = UUID(user_id_from_token)
        print("UUID from token:", uuid_from_token)
        print("String representation of UUID from token:", str(uuid_from_token))
    except ValueError as e:
        print("Error converting token user ID to UUID:", e)

    # Compare with the path parameter
    path_user_id = "dc9f498e-b24f-43d3-aff5-4398d90a4140"
    print("Path user ID:", path_user_id)
    print("Type of path user ID:", type(path_user_id))

    # Check if they are equal
    print("Are they equal?", user_id_from_token == path_user_id)

except JWTError as e:
    print("JWT Error:", e)