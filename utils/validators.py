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
