import requests

# make a GET request to a public API
response = requests.get("https://jsonplaceholder.typicode.com/users/1")

# check the status code of the response
print(response.status_code) # 200

# Parse the JSON response into a Python dictionary
data = response.json()

print(data["name"])           # Leanne Graham
print(data["email"])          # Sincere@april.biz