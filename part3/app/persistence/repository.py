#!/usr/bin/python3
"""Repository implementation - supports both in-memory and database persistence"""

from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract base class for repository pattern"""
    
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    """In-memory storage implementation - for development/testing"""
    
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """Add object to storage"""
        self._storage[str(obj.id)] = obj
        return obj

    def get(self, obj_id):
        """Get object by id"""
        return self._storage.get(str(obj_id))

    def get_all(self):
        """Return all objects"""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update object by id"""
        obj = self.get(obj_id)
        if not obj:
            return None

        for key, value in data.items():
            if hasattr(obj, key) and value is not None:
                setattr(obj, key, value)

        return obj

    def delete(self, obj_id):
        """Delete object by id"""
        return self._storage.pop(str(obj_id), None)

    def get_by_attribute(self, attr_name, attr_value):
        """Get object by attribute (e.g. email)"""
        return next(
            (obj for obj in self._storage.values()
             if getattr(obj, attr_name, None) == attr_value),
            None
        )


class SQLAlchemyRepository(Repository):
    """SQLAlchemy database implementation - for production"""
    
    def __init__(self, model):
        """
        Initialize repository with a SQLAlchemy model
        
        Args:
            model: SQLAlchemy model class (e.g., User, Place, Review, Amenity)
        """
        self.model = model

    def add(self, obj):
        """Add object to database"""
        from app.extensions import db
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Get object by id from database"""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Return all objects from database"""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update object by id in database"""
        from app.extensions import db
        obj = self.get(obj_id)
        if not obj:
            return None

        for key, value in data.items():
            if hasattr(obj, key) and value is not None:
                setattr(obj, key, value)
        
        db.session.commit()
        return obj

    def delete(self, obj_id):
        """Delete object by id from database"""
        from app.extensions import db
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return obj
        return None

    def get_by_attribute(self, attr_name, attr_value):
        """Get object by attribute from database"""
        return self.model.query.filter(
            getattr(self.model, attr_name) == attr_value
        ).first()