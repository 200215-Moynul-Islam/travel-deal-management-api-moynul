"""System Administration Service Layer."""

import urllib.parse
from database.models import db
from database.models import ApiRequestLog, TravelDeal

def get_api_analytics() -> dict:
    """Performs operation analysis based on log table.
    
    Returns:
        dict: A dictionary containing request analytics of the system.
    """

    all_logs = ApiRequestLog.query.all()
    most_viewed_deal = TravelDeal.query.filter(TravelDeal.view_count >= 1).order_by(TravelDeal.view_count.desc()).first()

    most_viewed_deal_data = None
    if most_viewed_deal:
        most_viewed_deal_data = most_viewed_deal.to_dict()

    total_requests = len(all_logs)
    successful_requests = 0
    for log in all_logs:
        if log.status_code >= 200 and log.status_code < 300:
            successful_requests += 1
    failed_requests = total_requests - successful_requests

    # 3. Parse and Tally Most Searched Destination from our in-memory list
    destination_counts = {}
    for log in all_logs:
        # Check if query_params has content
        if log.query_params and log.query_params.strip():
            parsed_params = urllib.parse.parse_qs(log.query_params)
            if 'destination' in parsed_params:
                # Standardize casing to group strings perfectly
                destination_value = parsed_params['destination'][0].strip().lower()
                destination_counts[destination_value] = destination_counts.get(destination_value, 0) + 1

    most_searched_destination = None
    highest_count = 0
    for destination, count in destination_counts.items():
        if count > highest_count:
            highest_count = count
            most_searched_destination = destination

    return {
        "total_requests": total_requests,
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "most_searched_destination": most_searched_destination,
        "most_viewed_deal": most_viewed_deal_data
    }