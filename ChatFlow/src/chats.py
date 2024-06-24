from ChatFlow import db
from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g, Blueprint
from ChatFlow.db import db_cli
from ChatFlow.chatbot import chatgpt_response
from bson import ObjectId
import json

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chats', methods=['GET'])
@auth_access
def get_chats():
    status_error = 404
    try:
        user_id = g.decoded_jwt['user_id']
        chat_id_arr = []
        for chat in db_cli['Chats'].find({'user_id': user_id}):
            chat_id_arr.append(str(chat['_id']))
        if not chat_id_arr:
            raise Exception("No chats found!")

        res_json = json.dumps(chat_id_arr, ensure_ascii=False).encode('utf8')
    except Exception as e:
        return Response(str(e), status=status_error)
    return Response(res_json, status=200, mimetype='application/json charset=utf-8')


@chat_bp.route('/chat/<chat_id>', methods=['GET'])
@auth_access
def get_chat(chat_id):
    error_status = 400
    try:
        user_id = g.decoded_jwt['user_id']
        chat = db_cli['Chats'].find_one({'_id': ObjectId(chat_id)})
        if chat['user_id'] != user_id:
            error_status = 403
            raise Exception('You do not have access to this conversation.')

        chat_messages = []
        for message in chat['messages']:
            mes_content = db_cli['Messages'].find_one({'_id': message})
            mes = {
                'chat_id': str(mes_content['chat_id']),
                'user_id': str(mes_content['user_id']),
                'message': mes_content['message']
            }
            chat_messages.append(mes)

        if not chat_messages:
            error_status = 404
            raise Exception("No chats found!")

        res_json = json.dumps(chat_messages, ensure_ascii=False).encode('utf8')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(res_json, status=200, mimetype='application/json charset=utf-8')


@chat_bp.route('/chats', methods=['POST'])
@auth_access
def new_message():
    try:
        # Get input messages from the request
        data = request.get_json()
        user_id = g.decoded_jwt['user_id']
        message = data['message']
        if data['chat_id']:
            chat_id = ObjectId(data['chat_id'])  # Retrieve conversation_id from request
        else:
            query = {
                'user_id': user_id,
                'messages': []
            }
            chat_id = db_cli['Chats'].insert_one(query).inserted_id

        # Save user message to database with conversation_id
        query = {
            'chat_id': chat_id,
            'user_id': user_id,
            'message': {"role": "user", "content": message}
        }
        message_id = db_cli["Messages"].insert_one(query).inserted_id

        # Add Message to chat
        db_cli['Chats'].update_one({'_id': chat_id}, {'$push': {'messages': message_id}})

        # Load conversation history
        chat = []
        for message in db_cli["Messages"].find({'chat_id': chat_id}):
            print(message)
            chat.append(message['message'])

        print(chat)
        # Generate response from ChatGPT
        response = chatgpt_response(chat)

        # Add AI response to messages and chat
        query = {
            'chat_id': chat_id,
            'user_id': user_id,
            'message': {"role": "assistant", "content": response}
        }
        response_id = db_cli["Messages"].insert_one(query).inserted_id
        db_cli['Chats'].update_one({'_id': chat_id}, {'$push': {'messages': response_id}})

        res_dict = {
            'chat_id': str(chat_id),
            'message': {"role": "assistant", "content": response}
        }
        res_json = json.dumps(res_dict, ensure_ascii=False).encode('utf8')

    except Exception as e:
        return Response(response=str(e), status=400)
    return Response(res_json, status=200, mimetype='application/json charset=utf-8')


@chat_bp.route('/chats/<chat_id>', methods=['DELETE'])
@auth_access
def delete_conversation(chat_id):
    error_status = 400
    try:
        # Get user data from token
        user_id = g.decoded_jwt['user_id']
        chat_id = ObjectId(chat_id)

        # Find if chat belongs to user
        if db_cli['Chats'].find_one({'_id': chat_id})['user_id'] != user_id:
            error_status=403
            raise Exception('You do not have access to this conversation.')

        # Delete specific conversation
        if not db_cli['Chats'].delete_one({'_id': chat_id}).deleted_count:
            error_status=500
            raise Exception('Chat could not be deleted.')

        # Delete all chat messages
        db_cli['Messages'].delete_many({'chat_id': chat_id})
    except Exception as e:
        return Response(response=str(e), status=error_status)
    return Response(status=204)
