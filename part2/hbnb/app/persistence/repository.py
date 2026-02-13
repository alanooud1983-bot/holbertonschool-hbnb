#!/usr/bin/python3
"""In-memory repository implementation"""

class Repository:
    def add(self, obj):
        raise NotImplementedError

    def get(self, obj_id):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def update(self, obj_id, data):
        raise NotImplementedError

    def delete(self, obj_id):
        raise NotImplementedError


class InMemoryRepository(Repository):
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
