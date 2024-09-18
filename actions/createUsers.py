import base64
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

MONGO_URI = 'mongodb+srv://mohamedalthaf872:MgDIcs8GevSto9Rz@immigrationchatbotclust.nuvxh.mongodb.net/?retryWrites=true&w=majority&appName=immigrationChatBotCluster'

client = MongoClient(MONGO_URI,tls=True,
    tlsAllowInvalidCertificates=True)
db = client['immigrationChatBotCluster']
users_collection = db['users']

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({'message': 'The server is running and connected successfully!'}), 200

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

    try:
        picture_data = picture_data.split(',')[1]
        picture_bytes = base64.b64decode(picture_data)
    except Exception as e:
        return jsonify({'error': 'Invalid picture data'}), 400

    filename = f"{username}_profile_picture.png"
    picture_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(picture_path, 'wb') as f:
        f.write(picture_bytes)

    hashed_password = generate_password_hash(password)

    user = {
        'email': email,
        'password': hashed_password,
        'picture': picture_path,
        'username': username
    }

    users_collection.insert_one(user)
    return jsonify({'message': 'User registered successfully!'}), 201



@app.route('/users', methods=['GET'])
def get_users():
    try:
        users_collection = client.db.users
        users = list(users_collection.find({}, {'_id': 0}))  # Exclude _id field
        return jsonify(users), 200
    except Exception as e:
        print(f"Error retrieving users: {e}")
        return jsonify({"error": "An error occurred while retrieving users"}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
