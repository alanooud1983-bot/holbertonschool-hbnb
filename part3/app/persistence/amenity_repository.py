"""
AmenityRepository - Handles amenity-specific database operations
Extends SQLAlchemyRepository with amenity-specific queries
"""
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """Repository for Amenity entity with custom amenity-specific methods"""
    
    def __init__(self):
        """Initialize AmenityRepository with Amenity model"""
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        """
        Find an amenity by name
        
        Args:
            name (str): Name of the amenity
            
        Returns:
            Amenity: Amenity object if found, None otherwise
        """
        return self.model.query.filter_by(name=name).first()
    
    def search_amenities(self, keyword):
        """
        Search amenities by keyword (case-insensitive)
        
        Args:
            keyword (str): Search keyword
            
        Returns:
            list: List of Amenity objects matching the keyword
        """
        return self.model.query.filter(
            self.model.name.ilike(f'%{keyword}%')
        ).all()
