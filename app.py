from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import tensorflow as tf
import numpy as np

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
    phoneNumber = int(data.get('phoneNumber'))
    password = data.get('pass')
    age = int(data.get('age'))
    weight = int(data.get('weight'))
    height = int(data.get('height'))
    gender=data.get("gender")
    guardianName = data.get('guardianName')
    guardianNo = int(data.get('guardianNo'))
    NeighbourName = data.get('NeighbourName')
    NeighbourNo=int(data.get("NeighbourNo"))
    HospitalName = data.get('HospitalName')
    HospitalNo=int(data.get("HospitalNo"))
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

@app.route('/api/predict', methods=['POST'])
def predict_with_model():
    data = request.get_json()
    accx = data.get('accx')
    accy = data.get('accy')
    accz = data.get('accz')
    gyrx = data.get('gyrx')
    gyry = data.get('gyry')
    gyrz = data.get('gyrz')
    lat=data.get("lat")
    long=data.get("long")
    age=data.get("age")
    height=data.get("height")
    weight=data.get("weight")
    gender=data.get("gender")
    g=0
    if gender=='Male':
        g=1
    # Load the model
    print(g)
    print(accx,accy,accz,gyrx,gyry,gyrz)
    model1 = tf.keras.models.load_model("Acc.h5")
    single_row_data_acc = np.array([[age,accx,accy, accz, height, weight, g]]).astype("float32")
    single_row_data_acc = single_row_data_acc.reshape(1, 7, 1)
    predictions = model1.predict(single_row_data_acc)
    # Example with a threshold of 0.5
    threshold = 0.5
    binary_prediction1 = (predictions > threshold).astype(int)
    print(binary_prediction1[0][0])
    model2 = tf.keras.models.load_model("Gyro.h5")
    single_row_data_gyro = np.array([[age,gyrx,gyry, gyrz, height, weight, g]]).astype("float32")
    single_row_data_gyro = single_row_data_gyro.reshape(1, 7, 1)
    predictions = model2.predict(single_row_data_gyro)
    # Example with a threshold of 0.5
    threshold = 0.5
    binary_prediction2 = (predictions > threshold).astype(int)
    print(binary_prediction2[0][0])

    # Print the binary prediction
    fall="Fall"
    if binary_prediction2[0][0]==0 and binary_prediction1[0][0]==0:
        fall="Not Fall"


    print(fall)
    result = {
        'prediction': fall,
        "latitude":lat,
        "longitude":long
        
    }

    return result

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    phoneNumber = int(data.get('phoneNumber'))
    password = data.get('pass')
    # Find the user in the database
    user = collection.find_one({"phoneNumber":phoneNumber})
    print(user)
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
