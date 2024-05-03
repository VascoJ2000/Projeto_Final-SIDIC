from abc import ABC, abstractmethod
from flask import Flask
from dotenv import load_dotenv
import socket
import random
import requests
import time
import signal

load_dotenv()


# Abstract Class responsible for server cohesion
class Server(ABC):
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.port = get_port()
        self.setup_signals()
        self.load_balancer = None

    @abstractmethod
    def setup_routes(self):
        pass

    # Makes sure there is a balancer and that it knows of the server's existence
    def connect_to_balancer(self, ip, port, max_attempts=12):
        for i in range(max_attempts):
            self.load_balancer = f'http://{ip}:{port}/'
            response = requests.get(self.load_balancer + str(self.port))
            if response.status_code == 200:
                return print(f'Server was added to load balancer')
            else:
                time.sleep(2)
        raise Exception(f'Server could not be added to load balancer list')

    def run_server(self):
        try:
            self.app.run(port=self.port)
        except Exception as e:
            print('Error: ' + str(e))

    # Handles the shutdown signal
    # Makes sure the server doesn't restart or runs endlessly
    def sig_handler(self, signum, frame):
        print("Received signal: ", signum)
        print("Closing server on port: ", str(self.port))
        # Clean up tasks here if necessary
        if requests.delete(self.load_balancer).status_code == 204:
            print('Server was removed from load balancer')
        exit()

    # Ties the handler to the shutdown commands/buttons
    def setup_signals(self):
        signal.signal(signal.SIGINT, self.sig_handler)
        signal.signal(signal.SIGTERM, self.sig_handler)


# Makes sure the server uses a port that is not being used and within a certain range
def get_port(start_port=6000, max_attempts=12, port_range=0):
    for i in range(max_attempts):
        port = random.randint(start_port, start_port + port_range)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            return port
        except OSError:
            pass
        finally:
            sock.close()
    raise Exception(f"Unable to bind port in {max_attempts} attempts")
