from flask import Flask, request, jsonify

app = Flask(__name__) # initiate the Flask application

# creating a route for the API endpoint
@app.route('/get-user/<user_id>') # creating a get route for the API endpoint with a dynamic user_id parameter
def get_user(user_id):

    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }

    extra = request.args.get("extra")

    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200  # return the user data as a JSON response


## creating a post request
@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()  # get the JSON data from the request body

    # Here you would typically save the user data to a database
    # For this example, we'll just return the received data with a success message

    response = {
        "message": "User created successfully",
        "user_data": data
    }

    return jsonify(response), 201  # return a JSON response with a 201 status code  

if __name__ == '__main__':  # run the Flask application # creating the flask server 
    app.run(debug=True)

