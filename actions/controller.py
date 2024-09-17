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
agent = Agent.load("/models/20240916-155306-sienna-pot.tar.gz", action_endpoint=action_endpoint)

@app.route('/send_message', methods=['POST'])
async def send_message():
    data = request.json
    session_id = data['session_id']
    text = data['text']

    print("Received message:", text)  # This should appear in your server logs

    # Await the response from the agent
    responses = await agent.handle_text(text, sender_id=session_id)
    
    # Check if the response contains an intent
    if responses and 'intent' in responses[0]:
        bot_responses = [{'text': response['text']} for response in responses]
    else:
        bot_responses = [{'text': 'I did not understand that. Could you please rephrase?'}]

    # Return the bot's response
    return jsonify(bot_responses)


if __name__ == '__main__':
    socketio.run(app, port=5005)
