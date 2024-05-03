from __main__ import app


@app.route('/user', methods=['GET'])
def get_user(user_id, email):
    pass


@app.route('/user', methods=['POST'])
def add_user():
    pass


@app.route('/user', methods=['PUT'])
def update_user():
    pass


@app.route('/user', methods=['DELETE'])
def delete_user():
    pass