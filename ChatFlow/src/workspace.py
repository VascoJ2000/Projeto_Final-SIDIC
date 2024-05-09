from __main__ import app
from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g
from ChatFlow.db import db_cli
from bson import ObjectId
import json


@app.route('/workspace', methods=['GET'])
@auth_access
def get_workspaces():
    error_status = 400
    try:
        email = g.decoded_jwt['email']
        res_dict = {'workspaces': []}  # Defines an array to place all the workspaces info that belong to user

        # For each array found in the database gets the info necessary and places it in the array
        for entry in db_cli['Workspace'].find({'email': email}):
            res_dict['workspaces'].append({
                'workspace_name': entry['workspace_name'],
                "workspace_id": str(entry['_id']),
                "root_folder": str(entry['root_folder'])
            })
        res_json = json.dumps(res_dict, ensure_ascii=False).encode('utf8')  # Ensures the json is readable
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(res_json, status=200, mimetype='application/json charset=utf-8')


@app.route('/workspace', methods=['POST'])
@auth_access
def create_workspace():
    error_status = 400
    try:
        user_id = g.decoded_jwt['user_id']
        email = g.decoded_jwt['email']
        workspace_name = request.get_json()['workspace_name']
        query = {
            'user_id': ObjectId(user_id),
            'email': email,
            'workspace_name': workspace_name,
            'root_folder': None
        }
        # Gets the workspace id, so it can be placed in the root folder
        workspace_id = db_cli['Workspace'].insert_one(query).inserted_id

        query = {
            'workspace_id': workspace_id,
            'name': 'root',
            'root_folder': None,
            'folders': [],
            'files': [],
            'is_root': True
        }
        # Gets the root folder id, so it can be placed back on the workspace info
        folder_id = db_cli['Folders'].insert_one(query).inserted_id

        # if anything goes wrong deletes everything, so it doesn't clog the database with useless data
        if not db_cli['Workspace'].update_one({'_id': workspace_id}, {'$set': {'root_folder': folder_id}}).modified_count:
            error_status = 500
            db_cli['Workspace'].delete_one({'_id': workspace_id})
            db_cli['Folders'].delete_one({'_id': folder_id})
            raise KeyError('Workspace could not be created')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(f'Workspace {workspace_name} created', status=200)


@app.route('/workspace', methods=['PUT'])
@auth_access
def update_workspace():  # Only changes the name
    error_status = 400
    try:
        req_json = request.get_json()
        workspace_id = req_json['workspace_id']
        workspace_name = req_json['workspace_name']
        query = {'_id': ObjectId(workspace_id)}
        new_values = {'$set': {'workspace_name': workspace_name}}

        updated_workspace = db_cli['Workspace'].update_one(query, new_values)
        if not updated_workspace.modified_count:
            error_status = 404
            raise KeyError('Workspace info could not updated at the moment!')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response('Workspace name updated', status=200)


@app.route('/workspace/<workspace>', methods=['DELETE'])
@auth_access
def delete_workspace(workspace):
    error_status = 400
    try:
        email = g.decoded_jwt['email']
        workspace = db_cli['Workspace'].find_one({'_id': ObjectId(workspace)})
        if not workspace:  # Confirms if that workspace exists
            error_status = 404
            raise KeyError('Workspace not found')

        if workspace['email'] != email:  # Confirms if the workspace belong to user
            error_status = 403
            raise KeyError('Email does not match the workspace')

        deleted_workspace = db_cli['Workspace'].delete_one({'_id': workspace['_id']})
        if not deleted_workspace.deleted_count:  # Checks if the workspace was deleted
            error_status = 503
            raise Exception('Workspace could not be deleted')

        deleted_folders = db_cli['Folders'].delete_many({'workspace_id': workspace['_id']})
        if deleted_folders.deleted_count <= 0:  # Confirms if at least the root folder was deleted
            error_status = 503
            raise Exception('Workspace folders could not be deleted')

    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(f'Workspace {workspace["workspace_name"]} successfully deleted', status=200)
