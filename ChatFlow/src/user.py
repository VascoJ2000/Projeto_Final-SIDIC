from __main__ import app
from ChatFlow.middleware.auth import auth_access
from flask import Response, request, g


@app.route('/user', methods=['GET'])
@auth_access
def get_user():
    email = g.decoded_jwt['email']
    return Response(email, status=200)


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