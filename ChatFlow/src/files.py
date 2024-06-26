from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g, Blueprint, send_file
from ChatFlow.db import db_cli, fs
from bson import ObjectId
from io import BytesIO
from ChatFlow.chatbot import chatgpt_response
import json
import PyPDF2
import fpdf

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


@files_bp.route('/file/resume/<file>', methods=['GET'])
@auth_access
def get_resume(file):
    error_status = 400
    try:
        file = ObjectId(file)
        email = g.decoded_jwt['email']
        user_id = g.decoded_jwt['user_id']
        file_info = fs.get(file)
        workspace_id = file_info.workspace_id

        if db_cli['Workspace'].find_one({'_id': workspace_id})['email'] != email:
            error_status = 403
            raise Exception('User not authorized to access this workspace')

        file_content = file_info.read()
        if not file_content:
            error_status = 404
            raise KeyError('File not found')

        text = pdf_to_text(file_content)
        text_sum = summarise_text(text)

        query = {
            'user_id': user_id,
            'name': file_info.filename + ' resume',
            'messages': []
        }
        chat_id = db_cli['Chats'].insert_one(query).inserted_id

        for message in text_sum:
            query = {
                'chat_id': chat_id,
                'user_id': user_id,
                'message': {"role": "assistant", "content": text_sum[message]}
            }
            mes_id = db_cli['Messages'].insert_one(query).inserted_id
            db_cli['Chats'].update_one({'_id': chat_id}, {'$push': {'messages': mes_id}})

        res_dict = {'chat_id': str(chat_id), 'name': file_info.filename + ' resume'}
        res_json = json.dumps(res_dict, ensure_ascii=False).encode('utf8')
    except Exception as e:
        return Response(str(e), status=error_status)
    return Response(res_json, status=200, mimetype='application/json charset=utf-8')


def pdf_to_text(file):
    pdf_stream = BytesIO(file)
    reader = PyPDF2.PdfReader(pdf_stream)
    pages = len(reader.pages)
    text = {}
    for page_num in range(pages):
        page = reader.pages[page_num]
        page_text = page.extract_text()
        text[page_num] = process_string(page_text)
    return text


def summarise_text(text, num_tokens=1000):
    text_sum = {}
    for page in text:
        print(text[page])
        mes = [{"role": "user", "content": f"Please summarize the following text: {text[page]}"}]
        text_sum[page] = chatgpt_response(mes, max_tokens=num_tokens)

    return text_sum


def text_to_pdf(text):
    pdf = fpdf.FPDF(format='A4')
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    for page in range(text):
        pdf.cell(200, 10, txt=text[page])
    return pdf


def process_string(string):
    string = string.lower()
    string = string.replace('\n', ' ')
    string = string.replace('\t', ' ')
    return string
