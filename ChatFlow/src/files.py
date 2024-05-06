from __main__ import app
from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g
from ChatFlow.db import db_cli
import json


@app.route('/file/<folder>&<file>', methods=['GET'])
@auth_access
def get_file():
    pass


@app.route('/file', methods=['POST'])
@auth_access
def post_file():
    pass


@app.route('/file', methods=['PUT'])
@auth_access
def put_file():
    pass


@app.route('/file', methods=['DELETE'])
@auth_access
def delete_file():
    pass