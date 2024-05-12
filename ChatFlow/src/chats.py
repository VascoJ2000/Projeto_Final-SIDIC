from __main__ import app
from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g
from dotenv import load_dotenv
from ChatFlow.db import db_cli
from ChatFlow.chatbot import chatgpt_response
from bson import ObjectId
import os
import sqlite3
import uuid  # Import UUID to generate unique conversation IDs

@app.route('/chatbot', methods=['POST'])
@auth_access
def chatbot():
    try:
        # Get input messages from the request
        data = request.get_json()
        user_id = g.decoded_jwt['user_id']  # para ser alterado
        print(user_id)
        message = data['message']
        conversation_id = data['conversation_id']  # Retrieve conversation_id from request

        # Save user message to database with conversation_id
        print(user_id)
        query = {
            'conversation_id': ObjectId(conversation_id),
            'user_id': user_id,
            'message': message,
        }
        message_id = db_cli["Messages"].insert_one(query).inserted_id

        # Load conversation history
        c.execute("SELECT message FROM chat_history WHERE user_id=? AND conversation_id=?", (user_id, conversation_id))
        history = c.fetchall()

        # Generate response from ChatGPT
        response = chatgpt_response([{"role": "user", "content": msg} for msg, in history])

        # Save ChatGPT response to database with conversation_id
        c.execute("INSERT INTO chat_history (user_id, conversation_id, message, response) VALUES (?, ?, ?, ?)",
                  (user_id, conversation_id, "", response))
        conn.commit()
    except Exception as e:
        return Response(response=str(e), status=400)

    return Response({"response": response}, status=200)


@app.route('/new_conversation', methods=['POST'])
@auth_access
def new_conversation():
    # Get input messages from the request
    data = request.json
    user_id = data.get('user_id')

    # Clear conversation history for the user and conversation
    c.execute("DELETE FROM chat_history WHERE user_id=? AND conversation_id=?", (user_id, conversation_id))
    conn.commit()

    return jsonify({"message": "New conversation started successfully!", "conversation_id": conversation_id})


@app.route('/delete_conversation', methods=['POST'])
@auth_access
def delete_conversation():
    # Get input data from the request
    data = request.json
    user_id = data.get('user_id')
    conversation_id = data.get('conversation_id')

    # Delete specific conversation
    c.execute("DELETE FROM chat_history WHERE user_id=? AND conversation_id=?", (user_id, conversation_id))
    conn.commit()

    return jsonify({"message": f"Conversation {conversation_id} deleted successfully!"})