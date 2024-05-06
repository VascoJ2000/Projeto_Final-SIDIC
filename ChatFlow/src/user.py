from __main__ import app
from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g
from ChatFlow.db import db_cli
import json


@app.route('/user', methods=['GET'])
@auth_access
def get_user():
    try:
        email = g.decoded_jwt['email']
        entry_data = db_cli['Users'].find_one({'email': email})
        if not entry_data:
            raise KeyError(f'User {email} could not be found pls try again later')
        user_id = g.decoded_jwt['user_id']
        res_dict = {'email': email,
                    'user_id': user_id,
                    'name': entry_data['name'],
                    'age': entry_data['age'],
                    'gender': entry_data['gender'],
                    'country': entry_data['country'],
                    'city': entry_data['city'],
                    'address': entry_data['address'],
                    'phone': entry_data['phone'],
                    'occupation': entry_data['occupation']
                    }
        res_json = json.dumps(res_dict, ensure_ascii=False).encode('utf8')
    except Exception as e:
        return Response(str(e), status=401)
    return Response(res_json, status=200, mimetype='application/json charset=utf-8')


@app.route('/user', methods=['PUT'])
@auth_access
def update_user():
    try:
        email = g.decoded_jwt['email']
        entry_data = db_cli['Users'].find_one({'email': email})
        if not entry_data:
            raise KeyError(f'User {email} could not be found pls try again later')

        req_data = request.get_json()
        new_values = {'$set': {}}
        for field in ['name', 'age', 'gender', 'country', 'city', 'address', 'phone', 'occupation']:
            if field in req_data:
                new_values['$set'][field] = req_data[field]

        updated_info = db_cli['Users'].update_one({'email': email}, new_values)
        if not updated_info.modified_count:
            raise KeyError(f'User {email} could not be updated')
    except Exception as e:
        return Response(str(e), status=401)
    return Response('User info successfully updated', status=200)


@app.route('/user', methods=['DELETE'])
@auth_access
def delete_user():
    try:
        error_status = 400
        email = g.decoded_jwt['email']
        entry_data = db_cli['Users'].find_one({'email': email})
        if not entry_data:
            error_status = 404
            raise KeyError(f'User {email} could not be found pls try again later')

        deleted_info = db_cli['Users'].delete_one({'email': email})
        if not deleted_info.deleted_count:
            error_status = 503
            raise KeyError(f'User {email} could not be deleted')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response('User account successfully deleted', status=200)
