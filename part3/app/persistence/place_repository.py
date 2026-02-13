"""
PlaceRepository - Handles place-specific database operations
Extends SQLAlchemyRepository with place-specific queries
"""
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place entity with custom place-specific methods"""
    
    def __init__(self):
        """Initialize PlaceRepository with Place model"""
        super().__init__(Place)

    def get_places_by_price_range(self, min_price, max_price):
        """
        Get places within a price range
        
        Args:
            min_price (float): Minimum price
            max_price (float): Maximum price
            
        Returns:
            list: List of Place objects within price range
        """
        return self.model.query.filter(
            self.model.price >= min_price,
            self.model.price <= max_price
        ).all()
    
    def get_places_by_location(self, latitude, longitude, radius=10.0):
        """
        Get places near a location (simplified - within a square boundary)
        
        Args:
            latitude (float): Center latitude
            longitude (float): Center longitude
            radius (float): Search radius (in degrees, approximate)
            
        Returns:
            list: List of Place objects near the location
        """
        lat_min = latitude - radius
        lat_max = latitude + radius
        lon_min = longitude - radius
        lon_max = longitude + radius
        
        return self.model.query.filter(
            self.model.latitude >= lat_min,
            self.model.latitude <= lat_max,
            self.model.longitude >= lon_min,
            self.model.longitude <= lon_max
        ).all()