"""
ReviewRepository - Handles review-specific database operations
Extends SQLAlchemyRepository with review-specific queries
"""
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """Repository for Review entity with custom review-specific methods"""
    
    def __init__(self):
        """Initialize ReviewRepository with Review model"""
        super().__init__(Review)

    def get_reviews_by_rating(self, rating):
        """
        Get all reviews with a specific rating
        
        Args:
            rating (int): Rating (1-5)
            
        Returns:
            list: List of Review objects with the specified rating
        """
        return self.model.query.filter_by(rating=rating).all()
    
    def get_reviews_by_rating_range(self, min_rating, max_rating):
        """
        Get reviews within a rating range
        
        Args:
            min_rating (int): Minimum rating
            max_rating (int): Maximum rating
            
        Returns:
            list: List of Review objects within rating range
        """
        return self.model.query.filter(
            self.model.rating >= min_rating,
            self.model.rating <= max_rating
        ).all()