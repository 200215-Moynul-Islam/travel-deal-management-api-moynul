"""Travel Deal Routes.

Maps HTTP request to correspoinding business service handlers.
"""

from http import HTTPStatus, HTTPMethod
from flask import Blueprint, request, jsonify
from services import deal_service
from utils import validators
import logging

deal_bp = Blueprint('deal_bp', __name__)

@deal_bp.route('', methods=[HTTPMethod.POST])
def add_deal():
    """Add a new travel deal"""
    data = request.get_json()

    validation_errors = validators.validate_deal_payload(data)
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

@deal_bp.route('', methods=[HTTPMethod.GET])
def get_all_deals():
    """Retrieve a collection listing of all saved travel deals."""
    all_deals = deal_service.get_all_deals()
    return jsonify({
        "status": "success",
        "data": all_deals
    }), HTTPStatus.OK

@deal_bp.route('<int:id>', methods=[HTTPMethod.GET])
def get_deal_by_id(id : int):
    """Retrieve a deal by id
    
    Args:
        id (int): Unique identifier of the travel deal.
    """

    deal = deal_service.get_deal_by_id(id)

    if not deal:
        return jsonify({
            "status": "error",
            "message": f"Travel deal with ID {id} not found."
        }), HTTPStatus.NOT_FOUND

    return jsonify({
        "status": "success",
        "data": deal
    }), HTTPStatus.OK

@deal_bp.route('/search', methods=[HTTPMethod.GET])
def search_travel_deals():
    """Retrieve travel deals filtered by provided search criteria."""

    query_params = request.args.to_dict()

    logging.info(f"Search request received with parameters: {query_params}")

    # Validate the query parameters
    validation_errors = validators.validate_search_query(query_params)
    if validation_errors:
        logging.warning(f"Search request failed validation: {validation_errors}")
        return jsonify({
            "status": "error",
            "errors": validation_errors
        }), HTTPStatus.BAD_REQUEST

    try:
        filtered_deals = deal_service.search_deals(query_params)
        logging.info(f"Search executed successfully.")
        return jsonify({
            "status": "success",
            "data": filtered_deals
        }), HTTPStatus.OK
        
    except Exception as e:
        logging.error(f"Internal server error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error."
        }), HTTPStatus.INTERNAL_SERVER_ERROR
