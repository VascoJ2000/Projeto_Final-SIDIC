from abc import ABC, abstractmethod
from flask import Flask
from dotenv import load_dotenv
import socket
import random
import requests
import time

load_dotenv()


class Server(ABC):
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.port = get_port()

    @abstractmethod
    def setup_routes(self):
        pass

    def connect_to_balancer(self, ip, port, max_attempts=12):
        for i in range(max_attempts):
            response = requests.get(f'http://{ip}:{port}/{self.port}')
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


def get_port(start_port=6000, max_attempts=12):
    for i in range(max_attempts):
        port = random.randint(start_port, start_port + 1999)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            return port
        except OSError:
            pass
        finally:
            sock.close()
    raise Exception(f"Unable to bind port in {max_attempts} attempts")