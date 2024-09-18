from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import json
from bson import ObjectId

app = Flask(__name__)
CORS(app)

MONGO_URI = 'mongodb+srv://mohamedalthaf872:MgDIcs8GevSto9Rz@immigrationchatbotclust.nuvxh.mongodb.net/?retryWrites=true&w=majority&appName=immigrationChatBotCluster'
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client['immigrationChatBotCluster']
users_collection = db['users']

def json_serializer(data):
    """Convert ObjectId to string for JSON serialization."""
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, dict):
        return {key: json_serializer(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [json_serializer(item) for item in data]
    else:
        return data

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    picture_data = data.get('picture')

    if not email or not password or not picture_data:
        return jsonify({'error': 'Please provide email, password, and picture'}), 400

    if users_collection.find_one({'email': email}):
        return jsonify({'error': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    users_collection.insert_one({
        'username': username,
        'email': email,
        'password': hashed_password,
        'picture': picture_data
    })

    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({'email': email})

    if not user:
        return jsonify({'error': 'User does not exist'}), 400

    if not check_password_hash(user['password'], password):
        return jsonify({'error': 'Incorrect password'}), 400

    return jsonify({'message': 'Login successful', 'user': json_serializer(user)}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
