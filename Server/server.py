from Server.controller import Controller
from Shared.Abstract.server import Server
import os


class BusinessLayerServer(Server):
    def __init__(self):
        self.controller = Controller()
        super().__init__()
        # TODO: Verify load balancer
        # self.connect_to_balancer(os.getenv('BL_LOAD_BALANCER_IP'), os.getenv('BL_LOAD_BALANCER_PORT'))
        self.run_server()

    def setup_routes(self):
        # Common Routes
        self.app.route('/<coll>&<entry_id>', methods=['GET'])(self.controller.get_entry)
        self.app.route('/all/<coll>', methods=['GET'])(self.controller.get_all_entries)
        self.app.route('/', methods=['POST'])(self.controller.add_entry)
        self.app.route('/', methods=['PUT'])(self.controller.update_entry)
        self.app.route('/<coll>&<entry_id>', methods=['DELETE'])(self.controller.delete_entry)

data_layer = DataLayerServer()