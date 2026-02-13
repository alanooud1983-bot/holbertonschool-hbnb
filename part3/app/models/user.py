from app.extensions import db, bcrypt
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel
import re


class User(BaseModel):
    __tablename__ = "users"

    # Core attributes (id, created_at, updated_at inherited from BaseModel)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    # One-to-Many: User can own many Places
    places = db.relationship(
        "Place", 
        backref="owner", 
        lazy=True, 
        cascade="all, delete-orphan"
    )
    
    # One-to-Many: User can write many Reviews
    reviews = db.relationship(
        "Review", 
        backref="user", 
        lazy=True, 
        cascade="all, delete-orphan"
    )

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()  # Initialize BaseModel (id, created_at, updated_at)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hash_password(password)

    @validates("first_name")
    def validate_first_name(self, key, value):
        """Validate first name - SQLAlchemy validator"""
        if not value or len(value) > 50:
            raise ValueError("First name is required and must be under 50 characters")
        return value

    @validates("last_name")
    def validate_last_name(self, key, value):
        """Validate last name - SQLAlchemy validator"""
        if not value or len(value) > 50:
            raise ValueError("Last name is required and must be under 50 characters")
        return value

    @validates("email")
    def validate_email(self, key, value):
        """Validate email format - SQLAlchemy validator"""
        email_regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
        if not re.match(email_regex, value):
            raise ValueError("Invalid email format")
        return value

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
