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
        # User Layer to Business Layer methods
        pass


data_layer = BusinessLayerServer()
