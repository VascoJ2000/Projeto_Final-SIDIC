from flask import render_template
from flask_cors import CORS
import signal
import sys
import ChatFlow

app = ChatFlow.create_app()
CORS(app)


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
