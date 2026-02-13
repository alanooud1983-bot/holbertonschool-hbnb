from app.extensions import db
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    __tablename__ = "amenities"

    # Core attributes (id, created_at, updated_at inherited from BaseModel)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # Many-to-Many: Amenity can be associated with many Places
    # The relationship is defined via backref in Place model using the place_amenity table

    def __init__(self, name):
        super().__init__()
        self.name = name

    @validates("name")
    def validate_name(self, key, value):
        """Validate name - SQLAlchemy validator"""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Amenity name must be a non-empty string")
        if len(value) > 50:
            raise ValueError("Amenity name must be at most 50 characters")
        return value.strip()

    def to_dict(self):
        """Convert amenity to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
