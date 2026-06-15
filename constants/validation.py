"""Validation Constants.

Organizes domain-specific business constraints into dedicated configuration classes.
"""

class TravelDealConstants:
    """Centralized constraints and allowed rules for the TravelDeal entity."""
    
    VALID_TYPES = ("Budget", "Luxury", "Adventure", "Family")
    MIN_RATING = 1.0
    MAX_RATING = 5.0

    ALLOWED_SORT_FIELD = "price"
