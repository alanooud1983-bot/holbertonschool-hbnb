# HBnB - Part 2: Business Logic and API Endpoints

## Description
This project is part of the HBnB application and focuses on implementing the **Business Logic layer** and **RESTful API endpoints** using Flask.  
The goal of this part is to build a clean, modular, and scalable backend architecture following best practices and the **Facade design pattern**.

An in-memory persistence layer is used in this stage and will be replaced by a database-backed solution in later parts.

---

## Learning Objectives
At the end of this project, you should be able to:
- Structure a Python project using a layered architecture.
- Apply the Facade design pattern to separate concerns.
- Implement core business logic entities and relationships.
- Build RESTful APIs using Flask-RESTX.
- Validate input data and handle errors correctly.
- Test API endpoints using black-box testing tools.

---

## Project Architecture
The application is organized into three main layers:

- **Presentation Layer**: Handles HTTP requests and responses (API).
- **Business Logic Layer**: Contains core entities, rules, and relationships.
- **Persistence Layer**: Manages data storage using an in-memory repository.

---

## Tasks

### 0. Project Setup and Package Initialization
- Created a modular project structure.
- Separated Presentation, Business Logic, and Persistence layers.
- Implemented an in-memory repository for object storage and validation.
- Prepared the Facade to manage communication between layers.

---

### 1. Core Business Logic Classes
- Implemented the core entities:
  - User
  - Place
  - Review
  - Amenity
- Defined attributes, relationships, and validation rules.
- Used base classes for shared attributes (e.g. id, timestamps).

---

### 2. User Endpoints
- Implemented API endpoints to manage users.
- Supported operations:
  - Create
  - Retrieve (all and by ID)
  - Update
- DELETE operation is not implemented for users.
- Integrated endpoints with the Business Logic layer via the Facade.

---

### 3. Amenity Endpoints
- Implemented endpoints to manage amenities.
- Supported operations:
  - Create
  - Retrieve
  - Update
- Business logic is fully separated from the API layer.

---

### 4. Place Endpoints
- Implemented endpoints to manage places.
- Handled relationships with:
  - Owner (User)
  - Amenities
- Added validation for attributes such as:
  - price
  - latitude
  - longitude
- Review management is excluded from this task.

---

### 5. Review Endpoints
- Implemented full CRUD operations for reviews.
- DELETE operation is supported only for reviews.
- Ensured each review is associated with:
  - A user
  - A place
- Updated the Place model to manage its reviews.

---

### 6. Testing and Validation
- Implemented validation rules for all entities.
- Performed black-box testing using `curl`.
- Generated Swagger documentation with Flask-RESTX.
- Wrote and executed unit tests using `unittest` or `pytest`.
- Documented successful and edge test cases.

---

## Technologies Used
- Python 3
- Flask
- Flask-RESTX
- RESTful API
- Facade Design Pattern
- In-memory data storage
- curl
- unittest / pytest

---

## Repository
- **GitHub repository**: `holbertonschool-hbnb`
- **Directory**: `part2`
