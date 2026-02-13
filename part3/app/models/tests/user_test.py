from app.models.user import User

"""
UserTester class to test multiple methods
"""

class UserTester:
    def test_user_creation(self):
        """Test valid user creation"""
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.is_admin is False
        assert isinstance(user.places, list)
        print("User creation test passed!")

    def test_admin_flag(self):
        """Test creating user as admin"""
        user = User("John", "Doe", "john@example.com", is_admin=True)
        assert user.is_admin
        print("test admin flag passed")

    def test_invalid_names(self):
        """Test empty or too long names"""
        try:
            User("", "Doe", "john@example.com")
        except ValueError as e:
            print("Empty first name:", e)

        try:
            User("John", "a"*51, "john@example.com")
        except ValueError as e:
            print("Long last name:", e)
        print("test_invalid_names passed")

    def test_email_validation(self):
        """Test invalid and valid emails"""
        invalid_emails = ["johnexample.com", "john@", "@example.com", "john@com"]
        for email in invalid_emails:
            try:
                User("John", "Doe", email)
            except ValueError as e:
                print(f"Invalid email '{email}':", e)

        valid_emails = ["john.doe@example.com", "jane_doe123@my-domain.co"]
        for email in valid_emails:
            user = User("Jane", "Doe", email)
            assert user.email == email
            print(f"Valid email '{email}' accepted")
        print("test_email_validation passed")


tester = UserTester()
tester.test_user_creation()
tester.test_admin_flag()
tester.test_invalid_names()
tester.test_email_validation()
