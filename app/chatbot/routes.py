from flask import Blueprint, request, jsonify
from datetime import datetime
from .db_services import *
# Assuming AI service functions are defined here
from .ai_services import get_query_response

chatbot_blueprint = Blueprint('chatbot_blueprint', __name__)


@chatbot_blueprint.route('/session/start', methods=['POST'])
def start_session():
    session_id = create_session()
    return jsonify({"session_id": str(session_id)})


@chatbot_blueprint.route('/session/end', methods=['POST'])
def end_session_route():
    session_id = request.json.get('session_id')
    end_session(session_id)
    return jsonify({"status": "Session ended"})


@chatbot_blueprint.route('/conversation/start', methods=['POST'])
def start_conversation_route():
    session_id = request.json.get('session_id')
    conversation_id = start_conversation(session_id)
    return jsonify({"conversation_id": str(conversation_id)})


@chatbot_blueprint.route('/conversation/end', methods=['POST'])
def end_conversation_route():
    conversation_id = request.json.get('conversation_id')
    end_conversation(conversation_id)
    return jsonify({"status": "Conversation ended"})


@chatbot_blueprint.route('/message/send', methods=['POST'])
def send_message():
    conversation_id = request.json.get('conversation_id')
    text = request.json.get('text')
    sender = request.json.get('sender')
    message_id = add_message(conversation_id, text, sender)
    return jsonify({"message_id": str(message_id)})


@chatbot_blueprint.route('/message/get', methods=['GET'])
def get_messages_route():
    conversation_id = request.args.get('conversation_id')
    messages = get_messages(conversation_id)
    return jsonify({"messages": messages})


@chatbot_blueprint.route('/query', methods=['POST'])
def handle_query():
    session_id = request.json.get('session_id')
    user_input = request.json.get('query')
    context = request.json.get('context', '')

    response = get_query_response(user_input, context)
    log_query(session_id, user_input, response, 'query_type')
    return jsonify({"response": response})
