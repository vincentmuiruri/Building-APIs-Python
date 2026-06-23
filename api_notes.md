# Python APIs: A Beginner's Complete Guide
### From Zero to Building, Using, and Connecting to APIs

---

## Table of Contents
1. What is an API?
2. How APIs Work (The Big Picture)
3. HTTP: The Language of APIs
4. Consuming APIs (Using APIs Others Built)
5. Building Your First API with Flask
6. Building a Better API with FastAPI
7. Authentication & Security
8. Connecting APIs Together
9. Common Patterns & Best Practices
10. Quick Reference Cheat Sheet

---

## 1. What is an API?

**API** stands for **Application Programming Interface**. In simple terms, it is a way for two programs to talk to each other.

Think of it like a restaurant:
- You (the client) look at a **menu** (the API documentation)
- You place an **order** (make a request)
- The kitchen (the server) **processes** it
- The waiter **brings back** your food (the response)

You never go into the kitchen yourself. You just use the menu to communicate.

### Real-World Examples
- When a weather app shows you today's forecast, it is calling a **weather API**
- When you "Sign in with Google," a website is using **Google's API**
- When you pay online, a **payment API** (like Stripe or M-Pesa's Daraja) handles the transaction

### Types of APIs
- **REST APIs** — The most common type. Uses HTTP. This guide focuses here.
- **GraphQL** — A flexible query language for APIs (more advanced)
- **WebSocket** — For real-time two-way communication (e.g., chat apps)
- **gRPC** — High-performance, used internally by big companies

---

## 2. How APIs Work (The Big Picture)

```
Your Code (Client)          The Internet           A Server (API)
      |                                                  |
      |  -------- HTTP Request (GET /users) --------->  |
      |                                                  |
      |  <------- HTTP Response (JSON data) ----------  |
      |                                                  |
```

Every API interaction has two sides:

- **Client** — The program making the request (your code, a mobile app, a browser)
- **Server** — The program listening and responding (the API you're calling)

The server exposes **endpoints** — specific URLs that do specific things.

```
https://api.example.com/users         → List all users
https://api.example.com/users/42      → Get user with ID 42
https://api.example.com/products      → List all products
```

---

## 3. HTTP: The Language of APIs

HTTP is the protocol (set of rules) that APIs use to communicate.

### HTTP Methods (Verbs)

| Method   | What it does             | Example                        |
|----------|--------------------------|--------------------------------|
| `GET`    | Retrieve data            | Get a list of users            |
| `POST`   | Create new data          | Create a new user              |
| `PUT`    | Replace existing data    | Update all fields of a user    |
| `PATCH`  | Update part of data      | Update only the user's email   |
| `DELETE` | Remove data              | Delete a user                  |

### HTTP Status Codes

The server always responds with a **status code** telling you what happened.

| Code | Meaning               | When you see it                      |
|------|-----------------------|--------------------------------------|
| 200  | OK                    | Request succeeded                    |
| 201  | Created               | New resource was created             |
| 400  | Bad Request           | You sent invalid data                |
| 401  | Unauthorized          | You need to log in / provide a key   |
| 403  | Forbidden             | You are logged in but not allowed    |
| 404  | Not Found             | The resource doesn't exist           |
| 422  | Unprocessable Entity  | Validation failed                    |
| 500  | Internal Server Error | Something broke on the server's side |

### JSON: The Data Format

Most REST APIs send and receive data in **JSON** (JavaScript Object Notation). Python handles it natively.

```json
{
  "id": 1,
  "name": "Alice Mwangi",
  "email": "alice@example.com",
  "is_active": true,
  "scores": [95, 87, 100]
}
```

JSON maps directly to Python dictionaries and lists:

```python
import json

# JSON string → Python dictionary
data = json.loads('{"name": "Alice", "age": 30}')
print(data["name"])   # Alice

# Python dictionary → JSON string
payload = {"city": "Nairobi", "country": "Kenya"}
json_string = json.dumps(payload)
print(json_string)   # {"city": "Nairobi", "country": "Kenya"}
```

---

## 4. Consuming APIs (Using APIs Others Built)

### Install the `requests` Library

```bash
pip install requests
```

This is the most popular Python library for making HTTP requests.

### Making a GET Request

```python
import requests

# Make a GET request to a public API
response = requests.get("https://jsonplaceholder.typicode.com/users/1")

# Check the status code
print(response.status_code)   # 200

# Parse the JSON response into a Python dict
data = response.json()
print(data["name"])           # Leanne Graham
print(data["email"])          # Sincere@april.biz
```

### Making a POST Request

```python
import requests

new_post = {
    "title": "My First Post",
    "body": "Hello from Python!",
    "userId": 1
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=new_post   # Automatically sets Content-Type: application/json
)

print(response.status_code)    # 201 (Created)
print(response.json())         # The created object, with an id assigned
```

### Passing Query Parameters

Query parameters go after a `?` in the URL. Use the `params` argument.

```python
import requests

# This calls: https://api.example.com/products?category=electronics&limit=10
response = requests.get(
    "https://api.example.com/products",
    params={"category": "electronics", "limit": 10}
)
```

### Sending Headers (e.g., API Keys)

Many APIs require you to send an API key in the request headers.

```python
import requests

headers = {
    "Authorization": "Bearer YOUR_API_KEY_HERE",
    "Content-Type": "application/json"
}

response = requests.get("https://api.example.com/data", headers=headers)
```

### Always Handle Errors

```python
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
```

### Practical Example: Weather API

```python
import requests

API_KEY = "your_openweathermap_key"
city = "Nairobi"

response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather",
    params={"q": city, "appid": API_KEY, "units": "metric"}
)

if response.status_code == 200:
    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    print(f"{city}: {temp}°C, {description}")
else:
    print("Failed to get weather data.")
```

---

## 5. Building Your First API with Flask

Flask is a lightweight Python web framework — great for learning.

### Install Flask

```bash
pip install flask
```

### Your First API (Hello World)

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to my API!"})

@app.route("/hello/<name>")
def hello(name):
    return jsonify({"greeting": f"Hello, {name}!"})

if __name__ == "__main__":
    app.run(debug=True)
```

Run it:
```bash
python app.py
```

Then open: `http://127.0.0.1:5000/hello/Alice` → `{"greeting": "Hello, Alice!"}`

### A Full CRUD API with Flask

CRUD = **C**reate, **R**ead, **U**pdate, **D**elete — the four fundamental operations.

```python
# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database" (a simple dictionary)
users = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob",   "email": "bob@example.com"},
}
next_id = 3

# READ — Get all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(list(users.values()))

# READ — Get one user
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

# CREATE — Add a new user
@app.route("/users", methods=["POST"])
def create_user():
    global next_id
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email are required"}), 400

    new_user = {"id": next_id, "name": data["name"], "email": data["email"]}
    users[next_id] = new_user
    next_id += 1
    return jsonify(new_user), 201

# UPDATE — Update a user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    users[user_id].update(data)
    return jsonify(users[user_id])

# DELETE — Remove a user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    del users[user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
```

### Testing Your API

Use `curl` in the terminal or the `requests` library:

```bash
# GET all users
curl http://127.0.0.1:5000/users

# CREATE a user
curl -X POST http://127.0.0.1:5000/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Carol", "email": "carol@example.com"}'

# DELETE a user
curl -X DELETE http://127.0.0.1:5000/users/1
```

Or with Python:
```python
import requests

base = "http://127.0.0.1:5000"

# Create
r = requests.post(f"{base}/users", json={"name": "Carol", "email": "carol@example.com"})
print(r.json())   # {"id": 3, "name": "Carol", ...}

# Read
r = requests.get(f"{base}/users/3")
print(r.json())
```

---

## 6. Building a Better API with FastAPI

FastAPI is modern, fast, and automatically generates documentation. It is the recommended choice for new projects.

### Install FastAPI

```bash
pip install fastapi uvicorn
```

### Your First FastAPI App

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI!"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"greeting": f"Hello, {name}!"}
```

Run it:
```bash
uvicorn main:app --reload
```

FastAPI **automatically generates** interactive docs at:
- `http://127.0.0.1:8000/docs` — Swagger UI (try your endpoints in the browser)
- `http://127.0.0.1:8000/redoc` — ReDoc documentation

### Full CRUD API with FastAPI and Data Validation

FastAPI uses **Pydantic models** to validate data automatically.

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI(title="Users API", version="1.0")

# ---- Data Model ----
class UserCreate(BaseModel):
    name: str
    email: str   # Use EmailStr if you install: pip install email-validator

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class User(BaseModel):
    id: int
    name: str
    email: str

# ---- In-memory store ----
users: dict[int, dict] = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob",   "email": "bob@example.com"},
}
next_id = 3

# ---- Endpoints ----

@app.get("/users", response_model=list[User])
def get_users():
    return list(users.values())

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.post("/users", response_model=User, status_code=201)
def create_user(user: UserCreate):
    global next_id
    new_user = {"id": next_id, **user.dict()}
    users[next_id] = new_user
    next_id += 1
    return new_user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True)   # Only update provided fields
    users[user_id].update(update_data)
    return users[user_id]

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return {"message": "User deleted"}
```

### Why FastAPI Over Flask?

| Feature               | Flask          | FastAPI             |
|-----------------------|----------------|---------------------|
| Automatic docs        | ❌ Manual       | ✅ Built-in          |
| Data validation       | ❌ Manual       | ✅ Pydantic          |
| Type hints support    | Partial        | ✅ Full              |
| Performance           | Good           | ✅ Very fast         |
| Learning curve        | Gentle         | Slightly steeper     |
| Best for              | Small projects | Production APIs      |

---

## 7. Authentication & Security

### API Keys (Simplest)

The client includes a secret key in the request header. The server checks it.

```python
# FastAPI example with API key check
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

VALID_API_KEYS = {"secret-key-123", "another-key-456"}

@app.get("/protected")
def protected_route(x_api_key: str = Header(...)):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return {"data": "This is protected data"}
```

Client sends:
```python
requests.get("http://localhost:8000/protected", headers={"x-api-key": "secret-key-123"})
```

### Bearer Tokens (JWT)

More secure and scalable. A token is issued at login and attached to every request.

```bash
pip install python-jose[cryptography] passlib
```

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "your-very-secret-key"   # In real apps, use an env variable!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Fake user database
fake_users = {"alice": {"username": "alice", "password": "password123"}}

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = fake_users.get(form.username)
    if not user or user["password"] != form.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def get_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return {"user": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Security Best Practices

- **Never hardcode secrets** — use environment variables
- **Always use HTTPS** in production
- **Validate all input** — never trust data from clients
- **Rate limit** your endpoints to prevent abuse
- **Log errors** but never expose stack traces to clients

```python
import os
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-for-dev-only")
```

---

## 8. Connecting APIs Together

One of the most powerful patterns is building an API that itself calls other APIs.

### Pattern: API Aggregator

```python
# main.py - An API that combines two external APIs
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/country-info/{country_code}")
def get_country_info(country_code: str):
    # Call external REST Countries API
    r = requests.get(f"https://restcountries.com/v3.1/alpha/{country_code}")
    if r.status_code != 200:
        return {"error": "Country not found"}

    country = r.json()[0]
    capital = country["capital"][0] if "capital" in country else "Unknown"

    return {
        "name": country["name"]["common"],
        "capital": capital,
        "population": country["population"],
        "region": country["region"],
    }
```

### Using Environment Variables for External Keys

```python
# .env file (never commit this to Git!)
WEATHER_API_KEY=abc123
DATABASE_URL=postgresql://...
```

```python
# Load it in Python
from dotenv import load_dotenv
import os

load_dotenv()   # Reads from .env file

API_KEY = os.getenv("WEATHER_API_KEY")
```

```bash
pip install python-dotenv
```

### Connecting to a Real Database

Replace the in-memory dictionary with a real database using SQLite.

```bash
pip install sqlalchemy
```

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session

engine = create_engine("sqlite:///mydb.sqlite")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

Base.metadata.create_all(engine)

# Create
with Session(engine) as session:
    new_user = User(name="Alice", email="alice@example.com")
    session.add(new_user)
    session.commit()

# Read
with Session(engine) as session:
    users = session.query(User).all()
    for u in users:
        print(u.name, u.email)
```

---

## 9. Common Patterns & Best Practices

### URL Structure Conventions

```
/users              — collection of users
/users/42           — specific user
/users/42/posts     — posts belonging to user 42
/users?active=true  — filter users (query param)
```

Always use **nouns** (not verbs) in URLs. The HTTP method is the verb.
```
✅  GET /users
❌  GET /getUsers

✅  DELETE /users/42
❌  POST /deleteUser
```

### Always Version Your API

```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

This lets you change the API without breaking existing users.

```python
# FastAPI with versioning
from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")
v2_router = APIRouter(prefix="/v2")

@v1_router.get("/users")
def get_users_v1():
    return [{"id": 1, "name": "Alice"}]

@v2_router.get("/users")
def get_users_v2():
    return {"data": [{"id": 1, "name": "Alice"}], "total": 1}

app.include_router(v1_router)
app.include_router(v2_router)
```

### Consistent Error Responses

Always return errors in the same shape:

```json
{
  "error": {
    "code": 404,
    "message": "User not found",
    "detail": "No user exists with id=99"
  }
}
```

### Add CORS for Browser Clients

If a browser (frontend) calls your API, you need CORS headers.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://myapp.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Project Structure (as your app grows)

```
my_api/
├── main.py              # App entry point
├── routers/
│   ├── users.py         # User-related routes
│   └── products.py      # Product-related routes
├── models/
│   └── user.py          # Pydantic + database models
├── database.py          # DB connection setup
├── auth.py              # Authentication logic
├── .env                 # Secrets (never commit!)
└── requirements.txt     # pip install -r requirements.txt
```

---

## 10. Quick Reference Cheat Sheet

### Consuming APIs

```python
import requests

# GET
r = requests.get(url, params={}, headers={}, timeout=5)

# POST / PUT / PATCH
r = requests.post(url, json={}, headers={})

# DELETE
r = requests.delete(url)

# Check response
r.status_code          # 200, 404, etc.
r.json()               # Parse JSON body
r.text                 # Raw text body
r.raise_for_status()   # Raise exception on error
```

### Flask Quickstart

```python
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/items", methods=["GET"])
def list_items():
    return jsonify([...])

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    return jsonify(data), 201

app.run(debug=True)   # http://127.0.0.1:5000
```

### FastAPI Quickstart

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"id": item_id}

@app.post("/items", status_code=201)
def create_item(item: Item):
    return item

# Run: uvicorn main:app --reload
# Docs: http://127.0.0.1:8000/docs
```

### HTTP Methods at a Glance

| Method   | Endpoint       | Action              |
|----------|----------------|---------------------|
| GET      | /users         | List all users      |
| GET      | /users/{id}    | Get one user        |
| POST     | /users         | Create a user       |
| PUT      | /users/{id}    | Replace a user      |
| PATCH    | /users/{id}    | Update part of user |
| DELETE   | /users/{id}    | Delete a user       |

---

## What to Learn Next

Once you are comfortable with these basics, explore:

1. **Databases** — PostgreSQL with SQLAlchemy or Tortoise ORM (async)
2. **Async FastAPI** — `async def` endpoints for high performance
3. **Testing** — `pytest` + `httpx` to write automated API tests
4. **Deployment** — Docker, Railway, Render, or Fly.io to host your API
5. **API Documentation** — OpenAPI spec, Postman collections
6. **Rate Limiting** — `slowapi` for Flask/FastAPI
7. **Caching** — Redis to speed up repeated requests
8. **Background Tasks** — Celery or FastAPI's `BackgroundTasks`

---

*Happy building! Every API you see in the real world follows these same fundamentals.*

