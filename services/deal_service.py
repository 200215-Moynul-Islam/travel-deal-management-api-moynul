"""Deal Management Service Layer.

Performs business logic for travel deals.
"""

from database.models import db
from database.models import TravelDeal

def create_new_deal(data: dict) -> dict:
    """Save a travel deal."""
    
    new_deal = TravelDeal(
        destination=data["destination"].strip(),
        price=float(data["price"]),
        platform=data["platform"].strip(),
        rating=float(data["rating"]),
        travel_type=data["travel_type"]
    )
    db.session.add(new_deal)
    db.session.commit()
    return new_deal.to_dict()

def get_all_deals() -> list:
    """Retrieve all travel deals."""

    deals = TravelDeal.query.all()
    return [deal.to_dict() for deal in deals]

def get_deal_by_id(id: int) -> dict:
    """Retrieve a travel deal by ID.

    Args:
        id (int): Unique identifier of the travel deal.
    
    Returns:
        dict: The deal data if found, or None if it doesn't exist.
    """
    # Look up the row directly by its primary key ID
    deal = TravelDeal.query.get(id)
    
    if not deal:
        return None
    
    return deal.to_dict()

def search_deals(query_params: dict) -> list:
    """Search travel deals using partial, case-insensitive matching.

    Args:
        query_params (dict): Query parameters for searching.

    Returns:
        list: A list of travel deal dictionaries satisfying the search criteria.
    """

    query = TravelDeal.query

    destination = query_params.get("destination")
    platform = query_params.get("platform")
    travel_type = query_params.get("travel_type")

    # Filter the deals based on provided query parameters
    if destination:
        query = query.filter(TravelDeal.destination.ilike(f"%{destination.strip()}%"))  
    if platform:
        query = query.filter(TravelDeal.platform.ilike(f"%{platform.strip()}%"))
    if travel_type:
        query = query.filter(TravelDeal.travel_type.ilike(f"%{travel_type.strip()}%"))

    filtered_deals = query.all()
    return [deal.to_dict() for deal in filtered_deals]
