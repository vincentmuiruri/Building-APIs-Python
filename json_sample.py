import json

# JSON string → Python dictionary
data = json.loads('{"name": "Alice","age": 30}')
print(data["name"])  # Output: Alice

# python dictonary to json string
payload = {"city": "Nairobi", "country": "Kenya"}
json_string = json.dumps(payload)
print(json_string)  # Output: {"city": "Nairobi", "country": "Kenya"}