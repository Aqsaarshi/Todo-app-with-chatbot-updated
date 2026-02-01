from jose import jwt
import os
from datetime import datetime, timedelta
from uuid import UUID

# Test JWT token creation and validation
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")  # Only for testing - ensure proper secret is set in production
ALGORITHM = os.getenv("ALGORITHM", "HS256")

print("Testing JWT token functionality...")
print(f"SECRET_KEY: {SECRET_KEY}")
print(f"ALGORITHM: {ALGORITHM}")

# Create a sample token
sample_user_id = "54ce415a-6014-46e5-9f15-7edfe877a4ef"
data = {"sub": sample_user_id}
expire = datetime.utcnow() + timedelta(minutes=30)
data.update({"exp": expire})

print(f"\nSample user ID: {sample_user_id}")
print(f"Expiration: {expire}")

try:
    # Encode the token
    encoded_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Encoded token: {encoded_token[:50]}...")  # Truncate for display
    
    # Decode the token
    decoded_payload = jwt.decode(encoded_token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Decoded payload: {decoded_payload}")
    
    # Extract user ID
    decoded_user_id = decoded_payload.get("sub")
    print(f"Decoded user ID: {decoded_user_id}")
    
    # Try to convert to UUID
    user_id_uuid = UUID(decoded_user_id)
    print(f"UUID conversion successful: {user_id_uuid}")
    
    print("\n[SUCCESS] JWT token functionality working correctly")
    
except Exception as e:
    print(f"\n[ERROR] Error with JWT functionality: {e}")
    import traceback
    traceback.print_exc()