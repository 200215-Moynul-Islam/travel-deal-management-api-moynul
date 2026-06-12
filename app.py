import os
from flask import Flask
from dotenv import load_dotenv

# Load configurations from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Import blueprints
    from routes import system_bp

    # Register blueprints
    app.register_blueprint(system_bp, url_prefix='')

    return app

if __name__ == '__main__':
    app = create_app()
    
    # Extract environment values
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    server_port = int(os.getenv('PORT', '5000'))

    app.run(debug=debug_mode, port=server_port)
