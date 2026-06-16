"""Database Models."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Create SQLAlchemy instance
db = SQLAlchemy()

class TravelDeal(db.Model):
    """Database schema table for storing travel deals."""

    __tablename__ = 'travel_deals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    destination = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    platform = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    travel_type = db.Column(db.String, nullable=False)
    view_count = db.Column(db.Integer, default=0, nullable=False)

    def to_dict(self) -> dict:
        """Transform SQL Alchemy object into a Python dictionary."""
        return {
            "id": self.id,
            "destination": self.destination,
            "price": self.price,
            "platform": self.platform,
            "rating": self.rating,
            "travel_type": self.travel_type
        }

class ApiRequestLog(db.Model):
    """Database schema table for storing request information."""

    __tablename__ = 'api_request_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(255), nullable=False)
    query_params = db.Column(db.Text, nullable=True)
    method = db.Column(db.String(10), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc), nullable=False)
