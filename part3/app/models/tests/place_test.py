from app.models.place import Place
from app.models.user import User
from app.models.review import Review

class PlaceTester:
    def test_place_creation(self):
        """Test valid place creation"""
        owner = User("Alice", "Smith", "alice.smith@example.com")
        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100,
            latitude=37.7749,
            longitude=-122.4194,
            owner=owner
        )

        assert place.title == "Cozy Apartment"
        assert place.description == "A nice place to stay"
        assert place.price == 100
        assert place.owner == owner
        assert isinstance(place.reviews, list)
        assert isinstance(place.amenities, list)
        print("Place creation test passed!")

    def test_invalid_title(self):
        """Check empty title and title longer than 100 characters"""
        owner = User("John", "Doe", "john.doe@example.com")
        try:
            Place("", "desc", 100, 0, 0, owner)
        except ValueError as e:
            print("Empty title:", e)

        try:
            Place("a"*101, "desc", 100, 0, 0, owner)
        except ValueError as e:
            print("Long title:", e)
        print("test_invalid_title passed")

    def test_invalid_price(self):
        """Check if price is 0 or negative"""
        owner = User("John", "Doe", "john.doe@example.com")
        try:
            Place("Nice Place", "desc", 0, 0, 0, owner)
        except ValueError as e:
            print("Zero price:", e)

        try:
            Place("Nice Place", "desc", -50, 0, 0, owner)
        except ValueError as e:
            print("Negative price:", e)
        print("test_invalid_price passed")

    def test_invalid_coordinates(self):
        """Check latitude and longitude boundaries"""
        owner = User("John", "Doe", "john.doe@example.com")
        try:
            Place("Nice Place", "desc", 100, -91, 0, owner)
        except ValueError as e:
            print("Latitude too low:", e)

        try:
            Place("Nice Place", "desc", 100, 91, 0, owner)
        except ValueError as e:
            print("Latitude too high:", e)

        try:
            Place("Nice Place", "desc", 100, 0, -181, owner)
        except ValueError as e:
            print("Longitude too low:", e)

        try:
            Place("Nice Place", "desc", 100, 0, 181, owner)
        except ValueError as e:
            print("Longitude too high:", e)
        print("test_invalid_coordinates passed")

    def test_invalid_owner(self):
        """Check if owner is valid User instance"""
        try:
            Place("Nice Place", "desc", 100, 0, 0, owner="NotAUser")
        except ValueError as e:
            print("Invalid owner:", e)
        print("test_invalid_owner passed")

    def test_add_review_and_amenity(self):
        """Test adding reviews and amenities"""
        owner = User("John", "Doe", "john.doe@example.com")
        reviewer = User("Jane", "Smith", "jane.smith@example.com")
        place = Place("Nice Place", "desc", 100, 0, 0, owner)
        
        review = Review("Great stay!", 5, place, reviewer)
        assert review in place.reviews, "Review should be added to place automatically"

        place.add_amenity("WiFi")
        assert "WiFi" in place.amenities
        place.add_amenity("WiFi") 
        assert place.amenities.count("WiFi") == 1
        print("test_add_review_and_amenity passed")
    
    def test_invalid_review(self):
        """Check if review is empty,
        or invalid rating """
        
        owner = User("John", "Doe", "john.doe@example.com")
        reviewer = User("Jane", "Smith", "jane.smith@example.com")
        place = Place("Nice Place", "desc", 100, 0, 0, owner)

        try:
            Review("", 5, place, reviewer)
        except ValueError as e:
            print("Empty review text:", e)

        try:
            Review("Good stay", 0, place, reviewer)
        except ValueError as e:
            print("Rating too low:", e)

        try:
            Review("Good stay", 6, place, reviewer)
        except ValueError as e:
            print("Rating too high:", e)

        print("test_invalid_review passed")


if __name__ == "__main__":
    tester = PlaceTester()
    tester.test_place_creation()
    tester.test_invalid_title()
    tester.test_invalid_price()
    tester.test_invalid_coordinates()
    tester.test_invalid_owner()
    tester.test_add_review_and_amenity()
    tester.test_invalid_review()
