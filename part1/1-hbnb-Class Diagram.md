<img width="842" height="617" alt="image" src="https://github.com/user-attachments/assets/f16a2bb2-6b16-43a0-af85-a58f7cb96206" />



# Detailed Class Diagram for Business Logic Layer

## Overview
This task models a system for managing **users, places, reviews, and amenities**.  

---

## Entities

### 1. User
**Role:** Represents system users, including both regular users and administrators. Users can create places and write reviews.  

**Key Attributes:**
- `id`: UUID, unique identifier  
- `first_name`, `last_name`, `email`  
- `password`: private, used for authentication  
- `is_admin`: boolean to identify administrators  
- `created_at`, `updated_at`: timestamps for audit purposes  

**Key Methods:**
- `register()`: create a new user  
- `update_info()`: update user profile  
- `delete()`: remove a user  

---

### 2. Place
**Role:** Represents properties listed for rent.  

**Key Attributes:**
- `id`: UUID  
- `title`, `description`  
- `price`: float  
- `latitude`, `longitude`: coordinates  
- `owner`: reference to the User who created the place  
- `amenities`: list of Amenity objects  
- `created_at`, `updated_at`: timestamps  

**Key Methods:**
- `create_place()`: add a new place  
- `update_place()`: modify an existing place  
- `delete_place()`: remove a place  
- `list_reviews()`: retrieve all reviews for this place  

---

### 3. Review
**Role:** Stores user feedback and ratings for places  

**Key Attributes:**
- `id`: UUID  
- `rate`: integer rating 
- `comment`: textual feedback  
- `user`: reference to the User who wrote the review  
- `place`: reference to the Place being reviewed  
- `created_at`, `updated_at`: timestamps  

**Key Methods:**
- `create_review()`: add a new review  
- `update_review()`: modify a review  
- `delete_review()`: remove a review  

---

### 4. Amenity
**Role:** Represents facilities or features available at places (e.g., Wi-Fi, pool).  

**Key Attributes:**
- `id`: UUID  
- `name`, `description`  
- `created_at`, `updated_at`: timestamps  

**Key Methods:**
- `create_amenity()`: add a new amenity  
- `update_amenity()`: modify an amenity  
- `delete_amenity()`: remove an amenity  
- `list_amenities()`: list all available amenities  

---

## Relationships
| Relationship | Description | Business Logic Contribution |
|--------------|-------------|----------------------------|
| User 1 --- * Place | A user can own multiple places | Users can manage multiple properties or listings |
| User 1 --- * Review | A user can write multiple reviews | Enables tracking of user activity and feedback |
| Place 1 --- * Review | A place can have multiple reviews | Aggregates feedback for quality and ratings |
| Place * --- * Amenity | Many-to-many; a place can have multiple amenities and an amenity can belong to multiple places | Flexible association of amenities to places without redundancy |


