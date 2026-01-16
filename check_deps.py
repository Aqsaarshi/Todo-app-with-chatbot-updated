import sys
import os

# Add backend to path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)

# Change to backend directory to load env
os.chdir(backend_path)

print("Backend directory exists:", os.path.exists('.'))

# Check if required modules can be imported
try:
    import dotenv
    print("dotenv imported successfully")
except ImportError as e:
    print(f"Failed to import dotenv: {e}")

try:
    import cohere
    print("cohere imported successfully")
except ImportError as e:
    print(f"Failed to import cohere: {e}")

try:
    import fastapi
    print("fastapi imported successfully")
except ImportError as e:
    print(f"Failed to import fastapi: {e}")

try:
    import sqlmodel
    print("sqlmodel imported successfully")
except ImportError as e:
    print(f"Failed to import sqlmodel: {e}")

# Check if the src directory exists
print("src directory exists:", os.path.exists('src'))
print("Contents of src:", os.listdir('src') if os.path.exists('src') else "Not found")

# Check if the services directory exists
services_path = os.path.join('src', 'services')
print("services directory exists:", os.path.exists(services_path))
if os.path.exists(services_path):
    print("Contents of services:", os.listdir(services_path))