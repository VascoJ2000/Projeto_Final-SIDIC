from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g, Blueprint, send_file
from ChatFlow.db import db_cli, fs
from bson import ObjectId, json_util
import json

files_bp = Blueprint('files', __name__)


@files_bp.route('/file/<file>', methods=['GET'])
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
    return send_file(file_content, as_attachment=True, mimetype='application/octet-stream', download_name=file_content.filename)


@files_bp.route('/file/<folder>', methods=['POST'])
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

        if not db_cli['Folders'].update_one({'_id': folder}, {'$push': {'files': {'file_id': file_id, 'name': file.filename}}}).modified_count:
            error_status = 404
            raise Exception('Root folder not found')

        res_json = json.dumps({'file_id': str(file_id), 'name': file.filename}, ensure_ascii=False).encode('utf8')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(res_json, status=200, mimetype='application/json charset=utf-8')


@files_bp.route('/file/<file>', methods=['DELETE'])
@auth_access
def delete_file(file):
    error_status = 400
    try:
        file = ObjectId(file)
        email = g.decoded_jwt['email']
        file_info = fs.get(file)
        workspace_id = file_info.workspace_id
        folder_id = file_info.root_folder

        if db_cli['Workspace'].find_one({'_id': workspace_id})['email'] != email:
            error_status = 403
            raise Exception('User not authorized to access this workspace')

        fs.delete(file)
        db_cli['Folders'].update_one({'_id': folder_id}, {'$pull': {'files': {'file_id': file}}})
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(None, status=204)
