"""Travel Deal Routes.

Maps HTTP request to correspoinding business service handlers.
"""

from http import HTTPStatus, HTTPMethod
from flask import Blueprint, request, jsonify
from services import deal_service
from utils.validators import validate_deal_payload

deal_bp = Blueprint('deal_bp', __name__)

@deal_bp.route('/deals', methods=[HTTPMethod.POST])
def add_deal():
    """Add a new travel deal"""
    data = request.get_json()

    validation_errors = validate_deal_payload(data)
    if validation_errors:
        return jsonify({
            "status": "error",
            "errors": validation_errors
        }, HTTPStatus.BAD_REQUEST)

    saved_deal = deal_service.create_new_deal(data)
    
    return jsonify({
        "status": "success",
        "data": saved_deal
    }), HTTPStatus.CREATED

@deal_bp.route('/deals', methods=[HTTPMethod.GET])
def get_all_deals():
    """Retrieve a collection listing of all saved travel deals."""
    all_deals = deal_service.get_all_deals()
    return jsonify({
        "status": "success",
        "data": all_deals
    }), HTTPStatus.OK
