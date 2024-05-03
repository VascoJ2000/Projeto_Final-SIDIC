from Server.controller import Controller
from Shared.Abstract.server import Server
import os


class BusinessLayerServer(Server):
    def __init__(self):
        self.controller = Controller()
        super().__init__()
        self.connect_to_balancer(os.getenv('BL_LOAD_BALANCER_IP'), os.getenv('BL_LOAD_BALANCER_PORT'))
        self.controller.cli.connect(os.getenv('DL_LOAD_BALANCER_IP'), os.getenv('DL_LOAD_BALANCER_PORT'))
        self.run_server()

    def setup_routes(self):
        # Auth methods
        self.app.route('/auth/login/<email>&<password>', methods=['GET'])(self.controller.login)
        self.app.route('/auth/signin', methods=['POST'])(self.controller.signin)
        self.app.route('/auth/logout', methods=['DELETE'])(self.controller.logout)
        self.app.route('/auth/token', methods=['GET'])(self.controller.token)
        self.app.route('/auth/email', methods=['POST'])(self.controller.verify_email)

        # User methods
        self.app.route('/user/<id>', methods=['GET'])(self.controller.get_user)
        self.app.route('/user', methods=['POST'])(self.controller.add_user)
        self.app.route('/user', methods=['PUT'])(self.controller.update_user)
        self.app.route('/user/<id>', methods=['DELETE'])(self.controller.delete_user)
