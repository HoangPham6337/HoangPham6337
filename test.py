import requests
import os

headers = {"Authorization": f"token {os.environ['GITHUB_TOKEN']}"}
print(os.environ["GITHUB_TOKEN"])
response = requests.get("http://api.github.com/user", headers=headers)
print(response.json())
if response.status_code == 200:
    print("✅ Authentication successful!")
    print(response.json())
elif response.status_code == 401:
    print("❌ Authentication failed! Possible causes:")
    print("- Invalid or expired token")
    print("- Missing necessary permissions")
    print("- Token not properly set in environment variables")
elif response.status_code == 403:
    print("❌ Rate limit exceeded! Try again later.")
else:
    print(f"Unexpected error: {response.status_code}")
    print(response.json())
