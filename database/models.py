"""Database Models."""

from flask_sqlalchemy import SQLAlchemy

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
