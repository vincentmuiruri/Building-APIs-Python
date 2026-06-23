import requests

new_post = {
    "title":"My First Post",
    "body":"Hello from Python!",
    "userId": 1
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=new_post   # Automatically sets Content-Type: application/json
)

print(response.status_code)  # 201 Created
print(response.json())       # The created object, with an id assigned