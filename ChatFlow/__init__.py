from flask import Flask


def create_app():
    app = Flask(__name__)

    # Import Blueprints
    from src.auth import auth_bp
    from src.chats import chat_bp
    from src.files import files_bp
    from src.folders import folder_bp
    from src.user import user_bp
    from src.workspace import workspace_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(folder_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(workspace_bp)

    return app