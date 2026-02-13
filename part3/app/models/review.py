from app.extensions import db
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel


class Review(BaseModel):
    __tablename__ = "reviews"

    # Core attributes (id, created_at, updated_at inherited from BaseModel)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    # Foreign Keys
    # Each review belongs to one User
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    # Each review belongs to one Place
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    
    # Note: Relationships 'user' and 'place' are created via backref in User and Place models

    def __init__(self, text, rating, user, place):
        super().__init__()
        # Validation
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text must be a non-empty string")
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        self.text = text.strip()
        self.rating = rating
        self.user = user
        self.place = place
        # user_id and place_id are set automatically via the relationships

    @validates("text")
    def validate_text(self, key, value):
        """Validate text - SQLAlchemy validator"""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Review text must be a non-empty string")
        return value.strip()

    @validates("rating")
    def validate_rating(self, key, value):
        """Validate rating - SQLAlchemy validator"""
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value

    def to_dict(self):
        """Convert review to dictionary"""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
