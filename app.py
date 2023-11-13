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
    username = data.get('name')
    phoneNumber = data.get('phoneNumber')
    password = data.get('pass')
    age = data.get('age')
    weight = data.get('weight')
    height = data.get('height')
    gender=data.get("gender")
    guardianName = data.get('guardianName')
    guardianNo = data.get('guardianNo')
    NeighbourName = data.get('NeighbourName')
    NeighbourNo=data.get("NeighbourNo")
    HospitalName = data.get('HospitalName')
    HospitalNo=data.get("HospitalNo")
    HospitalPref=data.get("HospPref")
    # print(data)
    

    # Check if the username already exists
    if collection.find_one({'username': username,"phoneNumber":phoneNumber}):
        return jsonify({'error': 'Username already exists'}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password, method='sha256')
    # Create a new user document
    user_data = {'username': username, 'password': hashed_password,'phoneNumber':phoneNumber,'age':age,'weight':weight,'height':height,'gender':gender,'guardianName':guardianName,'guardianNo':guardianNo,'NeighbourName':NeighbourName,'NeighbourNo':NeighbourNo,'HospitalName':HospitalName,'HospitalNo':HospitalNo,'HospitalPref':HospitalPref}
    try:
        collection.insert_one(user_data)
        user = collection.find_one({'username': username,"phoneNumber":phoneNumber})
        if user and check_password_hash(user['password'], password):
            user_details = {
                'user_id': str(user['_id']),
                'name': user['username'],
                'phoneNumber': user['phoneNumber'],
                'age':user['age'],
                'weight':user['weight'],
                'height':user['height'],
                'gender':user['gender'],
                'guardianName':user['guardianName'],
                'guardianNo':user['guardianNo'],
                'NeighbourName':user['NeighbourName'],
                'NeighbourNo':user['NeighbourNo'],
                'HospitalName':user['HospitalName'],
                'HospitalNo':user['HospitalNo'],
                'HospPref':user['HospitalPref'],
                # Add other user details as needed
            }
            return jsonify({'message': 'Login successful',"user_detail":user_details}), 200
    except Exception as e:
    # Handle connection error
        print(f"Error: {e}")

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('name')
    phoneNumber = data.get('phoneNumber')
    password = data.get('pass')
    # Find the user in the database
    user = collection.find_one({'username': username,"phoneNumber":phoneNumber})
    if user and check_password_hash(user['password'], password):
        user_details = {
            'user_id': str(user['_id']),
            'name': user['username'],
            'phoneNumber': user['phoneNumber'],
            'age':user['age'],
            'weight':user['weight'],
            'height':user['height'],
            'gender':user['gender'],
            'guardianName':user['guardianName'],
            'guardianNo':user['guardianNo'],
            'NeighbourName':user['NeighbourName'],
            'NeighbourNo':user['NeighbourNo'],
            'HospitalName':user['HospitalName'],
            'HospitalNo':user['HospitalNo'],
            'HospPref':user['HospitalPref'],
            # Add other user details as needed
        }
        return jsonify({'message': 'Login successful',"user_detail":user_details}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


if __name__ == '__main__':
    app.run(debug=True)
