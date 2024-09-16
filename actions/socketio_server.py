import asyncio
from flask import Flask,request, jsonify
from flask_socketio import SocketIO
from rasa.core.agent import Agent
from rasa.core.utils import EndpointConfig
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load("/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/models/20240916-152048-few-quarter.tar.gz", action_endpoint=action_endpoint)

@app.route('/send_message', methods=['POST'])
async def send_message():
    data = request.json
    session_id = data['session_id']
    text = data['text']

    print("Received message:", text)  # This should appear in your server logs

    # Await the response from the agent
    responses = await agent.handle_text(text, sender_id=session_id)

    # Prepare responses to return
    bot_responses = [{'text': response['text']} for response in responses]

    # Return the bot's response
    return jsonify(bot_responses)

if __name__ == '__main__':
    socketio.run(app, port=5005)
