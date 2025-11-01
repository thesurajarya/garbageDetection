from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

chatbot_bp = Blueprint('chatbot_bp', __name__)

@chatbot_bp.route('/api/chatbot', methods=['POST'])
def chatbot_reply():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if 'hello' in incoming_msg:
        msg.body("👋 Hi! Welcome to CleanCity Bot.\nSend an image of garbage or choke to report it.")
    else:
        msg.body("Send an image to report garbage 🗑️ or type 'help' for options.")

    return str(resp)
