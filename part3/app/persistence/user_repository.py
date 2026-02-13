"""
UserRepository - Handles user-specific database operations
Extends SQLAlchemyRepository with user-specific queries
"""
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Repository for User entity with custom user-specific methods"""
    
    def __init__(self):
        """Initialize UserRepository with User model"""
        super().__init__(User)
    
    def get_by_id(self, user_id):
        return self.session.query(User).filter_by(id=user_id).first()

    def get_user_by_email(self, email):
        """
        Find a user by email address
        
        Args:
            email (str): Email address to search for
            
        Returns:
            User: User object if found, None otherwise
        """
        return self.model.query.filter_by(email=email).first()
    
    def get_all_admins(self):
        """
        Get all admin users
        
        Returns:
            list: List of User objects where is_admin=True
        """
        return self.model.query.filter_by(is_admin=True).all()
    
    def get_all_regular_users(self):
        """
        Get all non-admin users
        
        Returns:
            list: List of User objects where is_admin=False
        """
        return self.model.query.filter_by(is_admin=False).all()
    