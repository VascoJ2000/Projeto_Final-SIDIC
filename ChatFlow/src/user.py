import json
from __main__ import app
from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g
from ChatFlow.db.client import db_cli


@app.route('/user', methods=['GET'])
@auth_access
def get_user():
    try:
        email = g.decoded_jwt['email']
        entry_data = db_cli.db['Users'].find_one({'email': email})
        if not entry_data:
            raise KeyError(f'User {email} could not be found pls try again later')
        name = entry_data['name']
        user_id = g.decoded_jwt['user_id']
        res_dict = {'email': email,
                    'user_id': user_id,
                    'name': name
                    }
        res_json = json.dumps(res_dict, ensure_ascii=False).encode('utf8')
    except Exception as e:
        return Response(str(e), status=401)
    return Response(res_json, status=200, mimetype='application/json charset=utf-8')


@app.route('/user', methods=['POST'])
@auth_access
def add_user():
    pass


@app.route('/user', methods=['PUT'])
@auth_access
def update_user():
    pass


@app.route('/user', methods=['DELETE'])
@auth_access
def delete_user():
    pass