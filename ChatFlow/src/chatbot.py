from flask import Flask, request, jsonify
from ChatFlow.middleware.auth import auth_access
from openai import OpenAI
from dotenv import load_dotenv
from ChatFlow.db.client import db_cli
import os
import sqlite3
import uuid  # Import UUID to generate unique conversation IDs

load_dotenv('.env')

app = Flask(__name__)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
model = "gpt-3.5-turbo-0125"
temperature = 0.7
max_tokens = 200


@app.route('/chatbot', methods=['POST'])
@auth_access
def chatbot():
    # Get input messages from the request
    data = request.json
    user_id = g.decoted_jwt('user_id') #para ser alterado
    message = data.get('message')
    conversation_id = data.get('conversation_id')  # Retrieve conversation_id from request
    
    # Save user message to database with conversation_id
    c.execute("INSERT INTO chat_history (user_id, conversation_id, message) VALUES (?, ?, ?)", (user_id, conversation_id, message))
    conn.commit()
    
    # Load conversation history
    c.execute("SELECT message FROM chat_history WHERE user_id=? AND conversation_id=?", (user_id, conversation_id))
    history = c.fetchall()
    
    # Generate response from ChatGPT
    response = chatgpt_response([{"role": "user", "content": msg} for msg, in history])
    
    # Save ChatGPT response to database with conversation_id
    c.execute("INSERT INTO chat_history (user_id, conversation_id, message, response) VALUES (?, ?, ?, ?)", (user_id, conversation_id, "", response))
    conn.commit()
    
    return jsonify({"response": response})

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

def chatgpt_response(messages):
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,  
    )
    return completion.choices[0].message.content
