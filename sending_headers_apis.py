# sending an API key in the request headers
# while handing the request headers always use error handling to avoid any unexpected errors

import requests

try:
    response = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=5)
    response.raise_for_status()   # Raises an exception for 4xx/5xx errors
    data = response.json()
    print(data)

except requests.exceptions.Timeout:
    print("The request timed out.")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")

except requests.exceptions.ConnectionError:
    print("Could not connect to the server.")
