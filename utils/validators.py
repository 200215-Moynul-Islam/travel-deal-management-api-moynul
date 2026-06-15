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
        errors.append(f"travel_type must be one of: {', '.join(TravelDealConstants.VALID_TYPES)}")

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
    
    #check for unknown travel type
    if travel_type:
        clean_travel_type = str(travel_type).strip()
        
        allowed_travel_types_lower = [t.lower() for t in TravelDealConstants.VALID_TYPES]
        
        if clean_travel_type.lower() not in allowed_travel_types_lower:
            errors.append(
                f"Unknown travel type: '{clean_travel_type}'. Allowed types are: {', '.join(TravelDealConstants.VALID_TYPES)}."
            )

    return errors

def validate_filter_query(data: dict) -> list:
    """Validate query parameters for filtering travel deals by budget.

    Args:
        data (dict): Query parameters' dictionary containing min_price and max_price.

    Returns:
        list: A list of error message strings. If empty, the payload is valid.
    """

    errors = []
    
    min_price_raw = data.get("min_price")
    max_price_raw = data.get("max_price")

    min_price = None
    max_price = None

    # Validate min_price if provided
    if min_price_raw is not None:
        try:
            min_price = float(min_price_raw)
            if min_price < 0:
                errors.append("Minimum price cannot be negative.")
        except ValueError:
            errors.append("Minimum price must be a valid number.")

    # Validate max_price if provided
    if max_price_raw is not None:
        try:
            max_price = float(max_price_raw)
            if max_price < 0:
                errors.append("Maximum price cannot be negative.")
        except ValueError:
            errors.append("Maximum price must be a valid number.")

    # Ensure max_price not less than min_price
    if min_price is not None and max_price is not None:
        if max_price < min_price:
            errors.append("Maximum price cannot be smaller than minimum price.")

    return errors

def validate_sort_query(data: dict) -> list:
    """Validate query parameters for sorting travel deals.

    Args:
        data (dict): Query parameters' dictionary containing sort_by and/or sort_order.

    Returns:
        list: A list of error message strings. If empty, the payload is valid.
    """

    errors = []
    
    sort_by = data.get("sort_by")
    sort_order = data.get("order")

    # Ensure sort_by is provided
    if not sort_by:
        errors.append("Missing required query parameter: 'sort_by'.")
        return errors

    if str(sort_by).strip().lower() != TravelDealConstants.ALLOWED_SORT_FIELD:
        errors.append(f"Invalid sorting field: '{sort_by}'. Only 'price' is allowed as sorting field.")

    # Validate sorting order
    allowed_orders = ["asc", "desc"]
    if sort_order is not None and sort_order.strip().lower() not in allowed_orders:
        errors.append(f"Invalid sorting order: '{sort_order}'. Allowed values are: 'asc' or 'desc'.")

    return errors
