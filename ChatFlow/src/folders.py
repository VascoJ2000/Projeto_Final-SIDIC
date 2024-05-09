from __main__ import app
from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g
from ChatFlow.db import db_cli
from bson import ObjectId
import json


@app.route('/folder/<folder>', methods=['GET'])
@auth_access
def get_folder(folder):
    error_status = 400
    try:
        folder_content = db_cli['Folders'].find_one({'_id': ObjectId(folder)})
        if not folder_content:
            error_status = 404
            raise KeyError('Folder not found')

        workspace = db_cli['Workspace'].find_one({'_id': folder_content['workspace_id']})
        email = g.decoded_jwt['email']
        if workspace['email'] != email:
            error_status = 403
            raise Exception('User not authorized to access this folder')

        root_folder = folder_content['root_folder']
        if folder_content['root_folder'] is not None:
            root_folder = str(root_folder)

        res_dict = {'folder_id': str(folder_content['_id']),
                    'folder_name': folder_content['name'],
                    'root_folder': root_folder,
                    'folders': folder_content['folders'],
                    'files': folder_content['files'],
                    'is_root': folder_content['is_root']
                    }
        res_json = json.dumps(res_dict, ensure_ascii=False).encode('utf8')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(res_json, status=200, mimetype='application/json charset=utf-8')


@app.route('/folder', methods=['POST'])
@auth_access
def create_folder():
    error_status = 400
    try:
        email = g.decoded_jwt['email']
        req_json = request.get_json()
        workspace_id = ObjectId(req_json['workspace_id'])
        root_folder = ObjectId(req_json['root_folder'])
        folder_name = req_json['folder_name']
        if db_cli['Folders'].find_one({'_id': root_folder})['workspace_id'] != workspace_id:
            error_status = 403
            raise Exception('Root folder does not belong to this workspace!')

        if db_cli['Workspace'].find_one({'_id': ObjectId(workspace_id)})['email'] != email:
            error_status = 403
            raise Exception('User not authorized to access this workspace')

        query = {'workspace_id': workspace_id,
                 'name': folder_name,
                 'root_folder': root_folder,
                 'folders': [],
                 'files': [],
                 'is_root': False
                 }
        folder_id = db_cli['Folders'].insert_one(query).inserted_id

        if not db_cli['Folders'].update_one({'_id': root_folder}, {'$push': {'folders': {'folder_id': folder_id, 'folder_name': folder_name}}}).modified_count:
            error_status = 404
            raise Exception('Root folder not found')

        res_dict = {'folder_id': str(folder_id), 'root_folder': str(root_folder), 'folder_name': folder_name}
        res_json = json.dumps(res_dict, ensure_ascii=False).encode('utf8')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(res_json, status=200, mimetype='application/json charset=utf-8')


@app.route('/folder', methods=['PUT'])
@auth_access
def update_folder():
    error_status = 400
    try:
        email = g.decoded_jwt['email']
        req_json = request.get_json()
        folder_id = ObjectId(req_json['folder_id'])
        folder_name = req_json['folder_name']
        workspace_id = db_cli['Folders'].find_one({'_id': folder_id})['workspace_id']
        workspace = db_cli['Workspace'].find_one({'_id': workspace_id})
        if workspace['email'] != email:
            error_status = 403
            raise Exception('User not authorized to access this workspace')

        if workspace['root_folder'] == folder_id:
            error_status = 403
            raise Exception('Root folder name cannot be updated')

        if not db_cli['Folders'].update_one({'_id': folder_id}, {'$set': {'name': folder_name}}).modified_count:
            error_status = 500
            raise Exception('Folder could not be updated at this moment!')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response('Folder successfully updated', status=200)


@app.route('/folder/<folder>', methods=['DELETE'])
@auth_access
def delete_folder(folder):
    error_status = 400
    try:
        email = g.decoded_jwt['email']
        folder_id = ObjectId(folder)
        folder_content = db_cli['Folders'].find_one({'_id': folder_id})

        if db_cli['Workspace'].find_one({'_id': folder_content['workspace_id']})['email'] != email:
            error_status = 403
            raise Exception('User not authorized to access this workspace')

        if not db_cli['Folders'].delete_one({'_id': folder_id}).deleted_count:
            error_status = 500
            raise Exception('Folder could not be deleted')

        if not db_cli['Folders'].update_one({'_id': folder_content['root_folder']}, {'$pull': {'folders': folder_id}}).modified_count:
            error_status = 500
            raise Exception('Folder could not be deleted properly!')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response('Folder successfully deleted', status=200)
