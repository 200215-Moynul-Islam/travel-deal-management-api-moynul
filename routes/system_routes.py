from http import HTTPStatus, HTTPMethod
from flask import Blueprint, jsonify

system_bp = Blueprint('system_bp', __name__)

@system_bp.route('/health', methods=[HTTPMethod.GET])
def health_check():
    """Verifies that the application is running.
    """
    return jsonify({
        "status": "success",
        "message": "Application is running."
    }), HTTPStatus.OK
