from flask import current_app
from datetime import datetime

db = current_app.mongo_db


def create_session():
    """Create a new session and return its ID."""
    session = {
        "start_time": datetime.now(),
        "status": "active"
    }

    return db.sessions.insert_one(session).inserted_id


def end_session(session_id):
    """Mark a session as ended."""
    update = {"$set": {"status": "ended", "end_time": datetime.now()}}
    return db.sessions.update_one({"_id": session_id}, update)


def get_session(session_id):
    """Retrieve a session by its ID."""
    return db.sessions.find_one({"_id": session_id})


def get_all_sessions():
    """Get all sessions"""
    return list(db.sessions.find())


def get_active_sessions():
    """Get all active sessions"""
    return list(db.sessions.find({"status": "active"}))


def get_ended_sessions():
    """Get all ended sessions"""
    return list(db.sessions.find({"status": "ended"}))


def start_conversation(session_id):
    """Start a new conversation linked to a session."""
    conversation = {
        "session_id": session_id,
        "start_time": datetime.now(),
        "status": "active"
    }
    return db.conversations.insert_one(conversation).inserted_id


def end_conversation(conversation_id):
    """End a conversation."""
    update = {"$set": {"status": "ended", "end_time": datetime.now()}}
    return db.conversations.update_one({"_id": conversation_id}, update)


def get_conversations(session_id):
    """Retrieve all conversations for a session."""
    return list(db.conversations.find({"session_id": session_id}))


def add_message(conversation_id, text, sender):
    """Add a message to a conversation."""
    message = {
        "conversation_id": conversation_id,
        "timestamp": datetime.now(),
        "text": text,
        "from_user": sender
    }
    return db.messages.insert_one(message).inserted_id


def get_messages(conversation_id):
    """Retrieve all messages in a conversation."""
    return list(db.messages.find({"conversation_id": conversation_id}).sort("timestamp", 1))


def log_query(session_id, query, response):
    """Log a user query and response."""
    log_entry = {
        "session_id": session_id,
        "query": query,
        "response": response,
        "timestamp": datetime.now()
    }
    return db.user_queries_log.insert_one(log_entry).inserted_id


def get_query_logs(session_id):
    """Retrieve all logs for a session."""
    return list(db.user_queries_log.find({"session_id": session_id}))


def get_all_query_logs():
    """Retrieve all logs"""
    return list(db.user_queries_log.find())
