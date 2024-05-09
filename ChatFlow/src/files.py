from __main__ import app
from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g
from ChatFlow.db import db_cli, fs
from bson import ObjectId, json_util
import json


@app.route('/file/<file>', methods=['GET'])
@auth_access
def get_file(file):
    error_status = 400
    try:
        file_content = fs.get(ObjectId(file))
        if not file_content:
            error_status = 404
            raise KeyError('File not found')

        workspace = db_cli['Workspace'].find_one({'_id': file_content.workspace_id})
        email = g.decoded_jwt['email']
        if workspace['email'] != email:
            error_status = 403
            raise Exception('User not authorized to access this file')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(file_content.read(), status=200, mimetype='application/octet-stream')


@app.route('/file/<folder>', methods=['POST'])
@auth_access
def post_file(folder):
    error_status = 400
    try:
        email = g.decoded_jwt['email']
        file = request.files['file']
        folder = ObjectId(folder)
        workspace_id = db_cli['Folders'].find_one({'_id': folder})['workspace_id']

        if db_cli['Workspace'].find_one({'_id': ObjectId(workspace_id)})['email'] != email:
            error_status = 403
            raise Exception('User not authorized to access this workspace')

        file_id = fs.put(file, filename=file.filename, root_folder=folder, workspace_id=workspace_id)

        if not db_cli['Folders'].update_one({'_id': folder}, {'$push': {'files': file_id}}).modified_count:
            error_status = 404
            raise Exception('Root folder not found')

        res_json = json.dumps({'file_id': str(file_id)}, ensure_ascii=False).encode('utf8')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(res_json, status=200, mimetype='application/json charset=utf-8')


@app.route('/file', methods=['PUT'])
@auth_access
def put_file():
    pass


@app.route('/file', methods=['DELETE'])
@auth_access
def delete_file():
    pass