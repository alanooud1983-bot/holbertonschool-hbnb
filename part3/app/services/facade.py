import os
from app.persistence.repository import InMemoryRepository
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        # Check environment variable to decide which repository to use
        use_database = os.getenv("USE_DATABASE", "False").lower() == "true"

        if use_database:
            # Production: Use database with specific repositories
            self.user_repo = UserRepository()
            self.place_repo = PlaceRepository()
            self.review_repo = ReviewRepository()
            self.amenity_repo = AmenityRepository()
        else:
            # Development: Use in-memory storage
            self.user_repo = InMemoryRepository()
            self.place_repo = InMemoryRepository()
            self.review_repo = InMemoryRepository()
            self.amenity_repo = InMemoryRepository()

    # --- Users ---
    def create_user(self, user_data):
        """Create a new user with hashed password"""
        password = user_data.pop("password", None)
        if not password:
            raise ValueError("Password is required")

        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=password,
            is_admin=user_data.get("is_admin", False)
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get user by email"""
        if hasattr(self.user_repo, 'get_user_by_email'):
            return self.user_repo.get_user_by_email(email)
        else:
            return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update user information"""
        return self.user_repo.update(user_id, user_data)

    # --- Places ---
    def create_place(self, place_data):
        """Create a new place with owner"""
        required = ["title", "price", "latitude", "longitude", "owner_id"]
        for key in required:
            if key not in place_data:
                raise ValueError(f"Missing required field: {key}")

        # Fetch the owner User object
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")

        # Create Place
        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update place information"""
        return self.place_repo.update(place_id, place_data)

    def delete_place(self, place_id):
        """Delete a place"""
        return self.place_repo.delete(place_id)

    def add_amenity_to_place(self, place_id, amenity_id):
        """Add an amenity to a place"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        
        # Add amenity to place
        place.add_amenity(amenity)
        
        # If using database, commit the change
        if hasattr(self.place_repo, 'update'):
            self.place_repo.update(place_id, {})
        
        return place

    # --- Reviews ---
    def create_review(self, review_data):
        """Create a new review with user and place relationships"""
        text = review_data.get("text")
        rating = review_data.get("rating")
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        if not text:
            raise ValueError("Review text is required")
        if not isinstance(rating, int):
            raise ValueError("Invalid review data")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be 1-5")
        
        # Validate and fetch user and place objects
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        # Create review with user and place objects (as constructor expects)
        review = Review(text=text, rating=rating, user=user, place=place)
        
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        place = self.place_repo.get(place_id)
        if not place:
            return []
        
        # If place has reviews relationship, return them
        if hasattr(place, 'reviews'):
            return place.reviews
        
        # Otherwise, filter all reviews by place_id
        all_reviews = self.review_repo.get_all()
        return [r for r in all_reviews if getattr(r, 'place_id', None) == place_id]

    def update_review(self, review_id, review_data):
        """Update review information"""
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review"""
        return self.review_repo.delete(review_id)

    # --- Amenities ---
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        name = amenity_data.get("name")
        if not name:
            raise ValueError("Amenity name is required")
        
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity information"""
        return self.amenity_repo.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        """Delete an amenity"""
        return self.amenity_repo.delete(amenity_id)