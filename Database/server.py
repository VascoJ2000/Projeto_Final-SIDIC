from Database.controller import Controller
from Shared.Abstract.server import Server
import os


class DataLayerServer(Server):
    def __init__(self):
        self.controller = Controller()
        super().__init__()
        self.connect_to_balancer(os.getenv('DB_LOAD_BALANCER_IP'), os.getenv('DB_LOAD_BALANCER_PORT'))
        self.run_server()

    def setup_routes(self):
        # Common Routes
        self.app.route('/<collection>&<identifier>&<entry_id>', methods=['GET'])(self.controller.get_entry)
        self.app.route('/', methods=['POST'])(self.controller.add_entry)
        self.app.route('/', methods=['PUT'])(self.controller.update_entry)
        self.app.route('/', methods=['DELETE'])(self.controller.delete_entry)
