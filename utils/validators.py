"""Validation Utilities.

Provides reusable validation logic.
"""

from constants import TravelDealConstants

def validate_deal_payload(data: dict) -> list:
    """Validate travel deal payloads.

    Returns:
        list: A list of error message strings. If empty, the payload is valid.
    """
    errors = []

    for field in ("destination", "price", "platform", "rating", "travel_type"):
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    # Return errors before proceeding if any field is missing
    if errors:
        return errors

    if not data["destination"].strip():
        errors.append("destination cannot be empty.")

    if data["price"] <= 0:
        errors.append("price must be a positive number.")

    if not data["platform"].strip():
        errors.append("platform cannot be empty.")

    if not (TravelDealConstants.MIN_RATING <= data["rating"] <= TravelDealConstants.MAX_RATING):
        errors.append(f"rating must be between {TravelDealConstants.MIN_RATING} and {TravelDealConstants.MAX_RATING}.")

    if data["travel_type"] not in TravelDealConstants.VALID_TYPES:
        errors.append(f"travel_type must be one of: {', '.join(sorted(TravelDealConstants.VALID_TYPES))}")

    return errors

def validate_search_query(data: dict) -> list:
    """Validate query parameters for searching travel deals.

    Args:
        data (dict): Query parameters' dictionary for searching travel deals.

    Returns:
        list: A list of error message strings. If empty, the payload is valid.
    """

    errors = []

    destination = data.get("destination")
    platform = data.get("platform")
    travel_type = data.get("travel_type")

    # Check for no query parameters
    if not destination and not platform and not travel_type:
        errors.append("Search query cannot be empty. Please provide at least one search filter ('destination', 'platform', or 'travel_type').")
        return errors

    # Check for empty query parameter value
    if destination is not None and not str(destination).strip():
        errors.append("Destination search term cannot be empty or whitespace.")
    if platform is not None and not str(platform).strip():
        errors.append("Platform search term cannot be empty or whitespace.")
    if travel_type is not None and not str(travel_type).strip():
        errors.append("Travel type search term cannot be empty or whitespace.")
    
    return errors
