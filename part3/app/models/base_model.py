from app.extensions import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """Base model with common attributes for all entities"""
    
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self):
        """Initialize base model with id and timestamps"""
        if not hasattr(self, 'id') or self.id is None:
            self.id = str(uuid.uuid4())
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = datetime.utcnow()
        if not hasattr(self, 'updated_at') or self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def update(self, data):
        """Update instance attributes from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()