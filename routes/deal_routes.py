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

@deal_bp.route('/<int:id>', methods=[HTTPMethod.PUT])
def update_deal_by_id(id: int):
    """Update a travel deal.

    Args:
        id (int): Unique identifier of the travel deal.
    """

    update_deal_payload = request.get_json()

    logging.info(f"Update request received with ID: {id} and payload: {update_deal_payload}")

    validation_errors = validators.validate_deal_payload(update_deal_payload)
    if validation_errors:
        logging.warning(f"Update request failed validation: {validation_errors}")
        return jsonify({
            "status": "error",
            "errors": validation_errors
        }), HTTPStatus.BAD_REQUEST

    try:
        updated_deal = deal_service.update_deal_by_id(id, update_deal_payload)

        if not updated_deal:
            logging.warning(f"Travel deal with ID {id} not found.")
            return jsonify({
                "status": "error",
                "message": f"Travel deal with ID {id} not found."
            }), HTTPStatus.NOT_FOUND
        
        logging.info(f"Update request executed successfully.")

        return jsonify({
            "status": "success",
            "data": updated_deal
        }), HTTPStatus.OK
    
    except Exception as e:
        logging.error(f"Internal server error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error."
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@deal_bp.route('', methods=[HTTPMethod.GET])
def get_all_deals():
    """Retrieve a collection listing of all saved travel deals."""
    all_deals = deal_service.get_all_deals()
    return jsonify({
        "status": "success",
        "data": all_deals
    }), HTTPStatus.OK

@deal_bp.route('/<int:id>', methods=[HTTPMethod.GET])
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

@deal_bp.route('/filter', methods=[HTTPMethod.GET])
def filter_travel_deals_by_budget():
    """Retrieve travel deals filtered by price range."""

    query_params = request.args.to_dict()
    
    logging.info(f"Filter request received with parameters: {query_params}")

    # Validate the query parameters
    validation_errors = validators.validate_filter_query(query_params)
    if validation_errors:
        logging.warning(f"Filter request failed validation: {validation_errors}")
        return jsonify({
            "status": "error",
            "errors": validation_errors
        }), HTTPStatus.BAD_REQUEST

    try:
        filtered_deals = deal_service.filter_deals_by_budget(query_params)

        logging.info(f"Filter executed successfully.")
        
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

@deal_bp.route('/sort', methods=[HTTPMethod.GET])
def get_sorted_travel_deals():
    """Retrieve sorted travel deals in ascendign or descending order."""

    query_params = request.args.to_dict()
    
    logging.info(f"Sort request received with parameters: {query_params}")

    # Validate the query parameters
    validation_errors = validators.validate_sort_query(query_params)
    if validation_errors:
        logging.warning(f"Sort request failed validation: {validation_errors}")
        return jsonify({
            "status": "error",
            "errors": validation_errors
        }), HTTPStatus.BAD_REQUEST

    try:
        sorted_deals = deal_service.get_sorted_deals(query_params)
        logging.info(f"Get sorted deals executed successfully.")
        return jsonify({
            "status": "success",
            "data": sorted_deals
        }), HTTPStatus.OK
        
    except Exception as e:
        logging.error(f"Internal server error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error."
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@deal_bp.route('/recent', methods=[HTTPMethod.GET])
def get_recently_viewed_deals():
    """Retrieve recently viewed deals."""

    logging.info(f"Get recently viewed deals request received.")

    try:
        recently_viewed_deals_deals = deal_service.get_recently_viewed_deals()
        logging.info(f"Get recently viewed deals executed successfully.")
        return jsonify({
            "status": "success",
            "data": recently_viewed_deals_deals
        }), HTTPStatus.OK
        
    except Exception as e:
        logging.error(f"Internal server error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error."
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@deal_bp.route('/<int:id>', methods=[HTTPMethod.DELETE])
def delete_deal_by_id(id: int):
    """Delete a travel deal.
    
    Args:
        id (int): Unique identifier of the travel deal.
    """

    logging.info(f"Delete deal request received.")

    try:
        success = deal_service.delete_deal_by_id(id)

        if not success:
            logging.warning(f"Deal with ID: {id} not found.")
            return jsonify({
                "status": "error",
                "message": f"Deal with ID: {id} not found."
            }), HTTPStatus.NOT_FOUND
        
        logging.info(f"Delete deal request executed successfully.")

        return jsonify({
            "status": "success",
            "data": None
        }), HTTPStatus.OK
    
    except Exception as e:
        logging.error(f"Internal server error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error."
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@deal_bp.route('/popular', methods=[HTTPMethod.GET])
def get_popular_deals():
    """Retrieve most viewed deals."""

    logging.info(f"Get popular deals request received.")

    try:
        popular_deals = deal_service.get_popular_deals()
        logging.info(f"Get popular deals executed successfully.")
        return jsonify({
            "status": "success",
            "data": popular_deals
        }), HTTPStatus.OK
    
    except Exception as e:
        logging.error(f"Internal server error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error."
        }), HTTPStatus.INTERNAL_SERVER_ERROR
