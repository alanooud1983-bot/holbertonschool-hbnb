# HBnB Part 3

## ER Digram 

![WhatsApp Image 2026-02-15 at 4 43 01 PM](https://github.com/user-attachments/assets/25f36890-985e-4383-8240-4b0e65517548)


## Project Structure

```
holbertonschool-hbnb/part3/
│
├── app/                          
│   ├── __init__.py             
│   ├── extensions.py            
│   │
│   ├── api/                     # API endpoints
│   │   └── v1/                  
│   │       ├── __init__.py      
│   │       ├── auth.py          # Login/authentication endpoints
│   │       ├── users.py         # User CRUD endpoints
│   │       ├── places.py        # Place CRUD endpoints
│   │       ├── reviews.py       # Review CRUD endpoints
│   │       └── amenities.py     # Amenity CRUD endpoints
│   │
│   ├── models/                  
│   │   ├── __init__.py
│   │   ├── base_model.py        
│   │   ├── user.py              # User model
│   │   ├── place.py             # Place model
│   │   ├── review.py            # Review model
│   │   ├── amenity.py           # Amenity model
│   │   └── tests/               # Model unit tests
│   │
│   ├── persistence/             
│   │   ├── __init__.py
│   │   ├── repository.py        
│   │   ├── user_repository.py   
│   │   ├── place_repository.py  
│   │   ├── review_repository.py 
│   │   └── amenity_repository.py
│   │
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   └── facade.py            
│   │
│   └── unit_test/               # API endpoint tests
│       ├── user_endpoint_test.py
│       ├── place_endpoint_test.py
│       ├── review_endpoint_test.py
│       └── amenitites_endpoint_test.py
│
├── sql/                         
│   ├── schema.sql              # Database schema (CREATE TABLE statements)
│   ├── data.sql               
│   └── generate_admin_hash.py  # Script to generate admin password hash
│
├── migrations/                  
│   ├── alembic.ini             
│   ├── env.py                  
│   ├── script.py.mako          
│   └── versions/               
│
├── config.py                    
├── run.py                       
├── requirements.txt             
├── .env                         
├── .gitignore                   
└── README.md                    
```

---

## Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/linawsm52/holbertonschool-hbnb/tree/a3469970b6495676323b37f3b161b062369cdd5d
cd holbertonschool-hbnb/part3
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create MySQL Database
```bash
mysql -u root -p
```

In MySQL prompt:
```sql
CREATE DATABASE hbnb_db;
EXIT;
```

### Step 5: Load Database Schema and Initial Data
```bash
mysql -u root -p
```

In MySQL prompt:
```sql
USE hbnb_db;
SOURCE sql/schema.sql;
SOURCE sql/data.sql;
SHOW TABLES;
EXIT;
```

### Step 6: Create Admin User

Generate the admin password hash:
```bash
python3 sql/generate_admin_hash.py
```

This will output a bcrypt hash. Copy it and update `sql/create_admin.sql`, then run:
```bash
mysql -u root -p hbnb_db < sql/create_admin.sql
```

### Step 7: Configure Environment Variables

Create a `.env` file in the project root:
```bash
DATABASE_URL=mysql+pymysql://root:password123@localhost/hbnb_db
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=development
```

### Step 8: Run Database Migrations
```bash
flask db upgrade
```

### Step 9: Run the Application
```bash
python3 run.py
```

The application will start at `http://127.0.0.1:5000`

---

## API Documentation

### Authentication

#### Login
```bash
POST /api/v1/login
Content-Type: application/json

{
  "email": "admin@hbnb.io",
  "password": "admin1234"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

export admin_token="PASTE_THE_TOKEN_HERE"
```

### test protected endpoint

```bash
curl -X GET http://127.0.0.1:5000/api/v1/protected \
  -H "Authorization: Bearer $admin_token"
```

### Users

```bash
GET    /api/v1/users              # List all users
GET    /api/v1/users/<id>         # Get user by ID
POST   /api/v1/users              # Create user
PUT    /api/v1/users/<id>         # Update user
DELETE /api/v1/users/<id>         # Delete user
```

### Places

```bash
GET    /api/v1/places             # List all places
GET    /api/v1/places/<id>        # Get place by ID
POST   /api/v1/places             # Create place (requires JWT)
PUT    /api/v1/places/<id>        # Update place (requires JWT)
DELETE /api/v1/places/<id>        # Delete place (requires JWT)
```

### Reviews

```bash
GET    /api/v1/reviews                  # List all reviews
GET    /api/v1/places/<id>/reviews      # Reviews for a place
POST   /api/v1/reviews                  # Create review (requires JWT)
PUT    /api/v1/reviews/<id>             # Update review (requires JWT)
DELETE /api/v1/reviews/<id>             # Delete review (requires JWT)
```

### Amenities

```bash
GET    /api/v1/amenities          # List all amenities
GET    /api/v1/amenities/<id>     # Get amenity by ID
POST   /api/v1/amenities          # Create amenity (admin only)
PUT    /api/v1/amenities/<id>     # Update amenity (admin only)
```


### Request Flow
```
HTTP Request
    ↓
API Endpoint (app/api/v1/users.py)
    ↓
Service/Facade (app/services/facade.py)
    ↓
Repository (app/persistence/user_repository.py)
    ↓
Model (app/models/user.py)
    ↓
Database (MySQL - hbnb_db)
    ↓
Response flows back up
```

### Database Schema

```sql
users:
├── id (UUID, Primary Key)
├── email (Unique, Not Null)
├── password (bcrypt hash)
├── first_name
├── last_name
├── is_admin (Boolean)
└── created_at, updated_at

places:
├── id (UUID, Primary Key)
├── name
├── description
├── address
├── city
├── latitude, longitude
├── user_id (Foreign Key → users)
└── created_at, updated_at

reviews:
├── id (UUID, Primary Key)
├── text
├── rating (1-5)
├── place_id (Foreign Key → places)
├── user_id (Foreign Key → users)
└── created_at, updated_at

amenities:
├── id (UUID, Primary Key)
├── name
└── created_at, updated_at

place_amenity (Many-to-Many):
├── place_id (Foreign Key → places)
└── amenity_id (Foreign Key → amenities)
```

---

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest app/unit_test/

# Run specific test file
python -m pytest app/unit_test/user_endpoint_test.py

```

### Test Database Connection

```bash
python3 -c 'from app import create_app; app = create_app(); print("MySQL connection successful")'
```

---
