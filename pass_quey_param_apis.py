import requests

# Using OpenLibrary API
response = requests.get(
    "https://openlibrary.org/search.json",
    params={
        "q": "python programming",
        "limit": 10
    }
)

print(response.status_code)
print(response.json())