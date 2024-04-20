from flask import Flask, request, jsonify
import hashlib


class LoadBalancer:
    def __init__(self, port):
        self.app = Flask(__name__)
        self.servers = []
        self.setup_routes()
        self.run_app(port)

    def add_server(self, port):
        try:
            server_ip = request.remote_addr
            server_port = port
            self.servers.append((server_ip, server_port))
            print(f"Server IP: {server_ip}, Server Port: {str(server_port)}")
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'message': 'Server was added successfully'}), 200

    def get_server(self):
        if len(self.servers) == 0:
            return '', 425
        try:
            ip_client = request.remote_addr
            server = self.hash_ip(ip_client)
        except Exception as e:
            return jsonify({'error': str(e)}), 406
        else:
            return jsonify({'Server_ip': server[0], 'Server_port': server[1]}), 200

    def hash_ip(self, ip_address):
        hashed_ip = hashlib.md5(ip_address.encode()).hexdigest()
        hashed_int = int(hashed_ip, 16)
        server_index = hashed_int % len(self.servers)
        return self.servers[server_index]

    def setup_routes(self):
        self.app.route('/', methods=['GET'])(self.get_server)
        self.app.route('/<port>', methods=['GET'])(self.add_server)

    def run_app(self, port):
        self.app.run(port=port)
        print(f'Load Balancer running on port {port}')
