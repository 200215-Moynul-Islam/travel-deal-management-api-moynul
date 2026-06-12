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
