from app.extensions import db
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel

# Association table for Many-to-Many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = "places"

    # Core attributes (id, created_at, updated_at inherited from BaseModel)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Foreign Key: Each place belongs to one owner (User)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    # One-to-Many: Place can have many Reviews
    reviews = db.relationship(
        "Review", 
        backref="place", 
        lazy=True, 
        cascade="all, delete-orphan"
    )
    
    # Many-to-Many: Place can have many Amenities
    amenities = db.relationship(
        "Amenity", 
        secondary=place_amenity, 
        lazy='subquery',
        backref=db.backref('places', lazy=True)
    )

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        # owner_id is set automatically via the relationship

    @validates("title")
    def validate_title(self, key, value):
        """Validate title - SQLAlchemy validator"""
        if not isinstance(value, str):
            raise TypeError("Title must be a string!")
        value = value.strip()
        if not value:
            raise ValueError("Title is required!")
        if len(value) > 100:
            raise ValueError("Title must be at most 100 characters!")
        return value

    @validates("description")
    def validate_description(self, key, value):
        """Validate description - SQLAlchemy validator"""
        if value is None:
            return ""
        if not isinstance(value, str):
            raise TypeError("Description must be a string!")
        return value.strip()

    @validates("price")
    def validate_price(self, key, value):
        """Validate price - SQLAlchemy validator"""
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number!")
        value = float(value)
        if value <= 0:
            raise ValueError("Price must be a positive value")
        return value

    @validates("latitude")
    def validate_latitude(self, key, value):
        """Validate latitude - SQLAlchemy validator"""
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number!")
        value = float(value)
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be within -90.0 to 90.0")
        return value

    @validates("longitude")
    def validate_longitude(self, key, value):
        """Validate longitude - SQLAlchemy validator"""
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number!")
        value = float(value)
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be within -180.0 to 180.0")
        return value

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    # Static validation methods (for backward compatibility)
    @staticmethod
    def _validate_title(value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string!")
        value = value.strip()
        if not value:
            raise ValueError("Title is required!")
        if len(value) > 100:
            raise ValueError("Title must be at most 100 characters!")
        return value

    @staticmethod
    def _validate_description(value):
        if value is None:
            return ""
        if not isinstance(value, str):
            raise TypeError("Description must be a string!")
        return value.strip()

    @staticmethod
    def _validate_price(value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number!")
        value = float(value)
        if value <= 0:
            raise ValueError("Price must be a positive value")
        return value

    @staticmethod
    def _validate_latitude(value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number!")
        value = float(value)
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be within -90.0 to 90.0")
        return value

    @staticmethod
    def _validate_longitude(value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number!")
        value = float(value)
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be within -180.0 to 180.0")
        return value
