from __main__ import app
from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g
from ChatFlow.db import db_cli
import json


@app.route('/workspace', methods=['GET'])
@auth_access
def get_workspaces():
    error_status = 400
    try:
        email = g.decoded_jwt['email']
        res_dict = {'workspaces': []}

        for entry in db_cli['Workspace'].find({'email': email}):
            res_dict['workspaces'].append(entry['workspace_name'])
        res_json = json.dumps(res_dict, ensure_ascii=False).encode('utf8')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(res_json, status=200, mimetype='application/json charset=utf-8')


@app.route('/workspace/<workspace>', methods=['GET'])
@auth_access
def get_workspace(workspace):
    pass


@app.route('/workspace', methods=['POST'])
@auth_access
def create_workspace():
    error_status = 400
    try:
        user_id = g.decoded_jwt['user_id']
        email = g.decoded_jwt['email']
        workspace_name = request.get_json()['workspace_name']
        query = {'user_id': user_id,
                 'email': email,
                 'workspace_name': workspace_name,
                 'folders': []
                 }
        workspace_id = db_cli['Workspace'].insert_one(query).inserted_id

        query = {'workspace_id': workspace_id,
                 'name': 'root',
                 'folders': [],
                 'files': []
                 }
        folder_id = db_cli['Folders'].insert_one(query).inserted_id

        db_cli['Workspace'].update_one({'_id': workspace_id}, {'$push': {'folders': folder_id}})
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(f'Workspace {workspace_name} created', status=200)


@app.route('/workspace', methods=['PUT'])
@auth_access
def update_workspace():
    pass


@app.route('/workspace', methods=['DELETE'])
@auth_access
def delete_workspace():
    pass
