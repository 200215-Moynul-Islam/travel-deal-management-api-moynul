from http import HTTPStatus, HTTPMethod
from venv import logger
from flask import Blueprint, jsonify

from services import system_service

system_bp = Blueprint('system_bp', __name__)

@system_bp.route('/health', methods=[HTTPMethod.GET])
def health_check():
    """Verifies that the application is running.
    """
    return jsonify({
        "status": "success",
        "message": "Application is running."
    }), HTTPStatus.OK

@system_bp.route('/stats', methods=[HTTPMethod.GET])
def get_stats():
    """Retrieve statistics of API request."""
    logger.info(f"Get stats request received.")
    try:
        analytics_data = system_service.get_api_analytics()
        logger.info(f"Get stats request executed successfully.")
        return jsonify(analytics_data), HTTPStatus.OK
        
    except Exception as e:
        logger.error(f"Internal server error")
        return jsonify({
            "status": "error",
            "error": "Internal server error."
        }), HTTPStatus.INTERNAL_SERVER_ERROR
