from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

# MongoDB configuration
# Replace with your MongoDB URI
MONGO_URI = 'mongodb+srv://vicky:vicky@cluster0.hsaut5j.mongodb.net/'
DB_NAME = 'Iot'
COLLECTION_NAME = 'users'

try:
    # Attempt to connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Check if the connection is successful
    print("Connected to MongoDB successfully!")

except Exception as e:
    # Handle connection error
    print(f"Error connecting to MongoDB: {e}")
# Connect to MongoDB using PyMongo


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the username already exists
    if collection.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password, method='sha256')

    # Create a new user document
    user_data = {'username': username, 'password': hashed_password}
    collection.insert_one(user_data)

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Find the user in the database
    user = collection.find_one({'username': username})

    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


if __name__ == '__main__':
    app.run(debug=True)
