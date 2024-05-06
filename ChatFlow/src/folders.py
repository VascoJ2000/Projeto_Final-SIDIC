from __main__ import app
from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g
from ChatFlow.db import db_cli
import json


@app.route('/folder/<workspace>&<folder>', methods=['GET'])
@auth_access
def get_folders(workspace, folder):
    pass


@app.route('/folder', methods=['POST'])
@auth_access
def create_folder(folder):
    pass


@app.route('/folder', methods=['PUT'])
@auth_access
def update_folder(folder):
    pass


@app.route('/folder', methods=['DELETE'])
@auth_access
def delete_folder(folder):
    pass
