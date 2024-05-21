from flask import Flask, render_template
from flask_cors import CORS
import signal
import sys

app = Flask(__name__)
CORS(app)

# import routes ***DON'T REMOVE***
import ChatFlow.src


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# Function to gracefully shut down the Flask server
def shutdown_server(signum, frame):
    print("Shutting down server...")
    sys.exit(0)


# Register signal handlers for SIGINT and SIGTERM
signal.signal(signal.SIGINT, shutdown_server)
signal.signal(signal.SIGTERM, shutdown_server)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=80)
