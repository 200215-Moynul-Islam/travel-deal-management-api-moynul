import os
from flask import Flask
from dotenv import load_dotenv
from database.models import db

# Load configurations from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///travel_deals.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Import blueprints
    from routes import system_bp, deal_bp

    # Register blueprints
    app.register_blueprint(system_bp, url_prefix='')
    app.register_blueprint(deal_bp, url_prefix='')

    return app

if __name__ == '__main__':
    app = create_app()
    
    # Extract environment values
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    server_port = int(os.getenv('PORT', '5000'))

    app.run(debug=debug_mode, port=server_port)
