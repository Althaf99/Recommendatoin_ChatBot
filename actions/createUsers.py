import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# MongoDB Atlas connection string
MONGO_URI = 'mongodb+srv://mohamedalthaf872:MgDIcs8GevSto9Rz@immigrationchatbotclust.nuvxh.mongodb.net/?retryWrites=true&w=majority&appName=immigrationChatBotCluster'
client = MongoClient(MONGO_URI)
db = client['user_database']
users_collection = db['users']

# Directory to save uploaded pictures
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed extensions for picture upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/register', methods=['POST'])
def register_user():
    print("HELOOL  WORLDSS")
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    # picture = request.files.get('picture')

    # if not email or not password or not picture:
    #     return jsonify({'error': 'Please provide email, password, and picture'}), 400

    if users_collection.find_one({'email': email}):
        return jsonify({'error': 'Email already exists'}), 409

    # if allowed_file(picture.filename):
    #     filename = secure_filename(picture.filename)
    #     picture_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #     picture.save(picture_path)
    # else:
        return jsonify({'error': 'Invalid file type'}), 400

    hashed_password = generate_password_hash(password)

    user = {
        'email': email,
        'password': hashed_password,
        # 'picture': picture_path,
        'username': username
    }

    users_collection.insert_one(user)
    return jsonify({'message': 'User registered successfully!'}), 201

if __name__ == '__main__':
    app.run(port=5000, debug=True)
