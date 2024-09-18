import asyncio
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from rasa.core.agent import Agent
from rasa.core.utils import EndpointConfig
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load("/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/models/20240918-213316-wintry-style.tar.gz", action_endpoint=action_endpoint)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    session_id = data.get('session_id')
    text = data.get('text')

    if not session_id or not text:
        return jsonify({'error': 'Invalid input'}), 400

    # Handle text using Rasa agent
    async def handle_text():
        return await agent.handle_text(text, sender_id=session_id)

    responses = asyncio.run(handle_text())

    if responses:
        bot_responses = [{'text': response['text']} for response in responses if 'text' in response]
    else:
        bot_responses = [{'text': 'I did not understand that. Could you please rephrase?'}]

    return jsonify(bot_responses)

if __name__ == '__main__':
    socketio.run(app, port=5005)
