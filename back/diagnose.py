# """
# Quick diagnostic script to check if FastAPI is running properly
# Run this while your server is running in another terminal
# """
# import requests
# import sys

# def check_endpoint(url, name):
#     try:
#         response = requests.get(url, timeout=5)
#         print(f"✓ {name}: Status {response.status_code}")
#         if response.status_code == 200:
#             print(f"  Response: {response.json()}")
#         return True
#     except requests.exceptions.ConnectionError:
#         print(f"✗ {name}: Cannot connect - is the server running?")
#         return False
#     except Exception as e:
#         print(f"✗ {name}: Error - {str(e)}")
#         return False

# print("=" * 50)
# print("FastAPI Server Diagnostic")
# print("=" * 50)
# print()

# base_url = "http://127.0.0.1:8000"

# # Check if server is running
# print("Checking server endpoints...")
# print()

# check_endpoint(f"{base_url}/", "Root endpoint")
# check_endpoint(f"{base_url}/health", "Health check")
# check_endpoint(f"{base_url}/docs", "Swagger UI")
# check_endpoint(f"{base_url}/redoc", "ReDoc")
# check_endpoint(f"{base_url}/openapi.json", "OpenAPI schema")

# print()
# print("=" * 50)
# print("If all checks pass, open browser to:")
# print(f"  {base_url}/docs")
# print("=" * 50)