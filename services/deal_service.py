"""Deal Management Service Layer.

Performs business logic for travel deals.
"""

from collections import deque
from database.models import db
from database.models import TravelDeal

# In memeory store to remember recently viewed deals
MAX_RECENTLY_VIEWED_DEALS = 10
RECENTLY_VIEWED_DEAL_IDS = deque(maxlen=MAX_RECENTLY_VIEWED_DEALS)

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
    
    # Add to recently viewed deal IDs store
    add_to_recently_viewed_deals_list(id)
    
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

def filter_deals_by_budget(query_params: dict) -> list:
    """Filter travel deals by price range.

    Args:
        query_params (dict): Query parameters for filtering.

    Returns:
        list: A list of travel deal dictionaries filtered by price range.
    """
    query = TravelDeal.query

    min_price = query_params.get("min_price")
    max_price = query_params.get("max_price")

    # Filter the deals based on provided query parameters
    if min_price is not None and min_price != "":
        query = query.filter(TravelDeal.price >= float(min_price))
        
    if max_price is not None and max_price != "":
        query = query.filter(TravelDeal.price <= float(max_price))

    filtered_deals = query.all()
    return [deal.to_dict() for deal in filtered_deals]

def get_sorted_deals(query_params: dict) -> list:
    """Sort travel deals in ascending or descending order.

    Args:
        query_params (dict): Query parameters for sorting.

    Returns:
        list: A list of sorted travel deal dictionaries.
    """

    query = TravelDeal.query

    sort_field = str(query_params.get("sort_by")).strip().lower()
    sort_order = str(query_params.get("order")).strip().lower()

    model_attribute = getattr(TravelDeal, sort_field, None)

    if model_attribute is not None:
        if sort_order == "desc":
            query = query.order_by(model_attribute.desc())
        else:
            query = query.order_by(model_attribute.asc()) # Sort in ascending order when order is not provided

    results = query.all()
    return [deal.to_dict() for deal in results]

def add_to_recently_viewed_deals_list(deal_id: int) -> None:
    if deal_id not in RECENTLY_VIEWED_DEAL_IDS:
        RECENTLY_VIEWED_DEAL_IDS.append(deal_id)

def get_recently_viewed_deals() -> list:
    """Retrieve recently viewed deals."""

    if not RECENTLY_VIEWED_DEAL_IDS:
        return []
    
    recently_viewed_deals = TravelDeal.query.filter(TravelDeal.id.in_(RECENTLY_VIEWED_DEAL_IDS)).all()

    return [deal.to_dict() for deal in recently_viewed_deals]
