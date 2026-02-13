# HBnB Evolution

## Project Overview
HBnB Evolution is a simplified AirBnB-like application designed to demonstrate the architecture, design, and implementation of a multi-layered software system. The project is divided into multiple parts, each focusing on a specific phase of the software development lifecycle.

1. **Part 1**: Architecture & UML Design
2. **Part 2**: Business Logic & API Implementation
3. **Part 3**: Authentication & Database Integration
4. **Part 4**: Frontend Web Client

---

## Features

### User Management
- User registration and profile management
- Role-based access control (Admin/Regular users)
- JWT-based authentication
- Secure password hashing with bcrypt

### Place Management
- Property listing creation and management
- Detailed place information (name, description, price, location)
- Geolocation support (latitude/longitude)
- Amenity associations

### Review Management
- User reviews for visited properties
- Star rating system (1-5)
- Comment functionality

### Amenity Management
- Many-to-many relationships with places

---

## Project Structure

```
holbertonschool-hbnb/
│
├── part1/                          # Phase 1: UML & Architecture
│   ├── 1-hbnb-Class Diagram.md    # UML class diagrams
│   └── README.md                   # Design documentation
│
├── part2/                          # Phase 2: Business Logic & API
│   └── hbnb/
│       ├── app/
│       │   ├── api/               # API endpoints (in-memory)
│       │   ├── models/            # Business logic models
│       │   ├── persistence/       # In-memory repository
│       │   └── services/          # Facade pattern
│       ├── config.py
│       ├── run.py
│       └── README.md
│
├── part3/                          # Phase 3: Auth & Database
│   ├── app/
│   │   ├── api/v1/                # RESTful API endpoints
│   │   │   ├── auth.py           # Authentication
│   │   │   ├── users.py          # User CRUD
│   │   │   ├── places.py         # Place CRUD
│   │   │   ├── reviews.py        # Review CRUD
│   │   │   └── amenities.py      # Amenity CRUD
│   │   ├── models/                # SQLAlchemy models
│   │   ├── persistence/           # Database repositories
│   │   └── services/              # Business logic layer
│   ├── sql/
│   │   ├── schema.sql            # Database schema
│   │   ├── data.sql              # Initial data
│   │   └── generate_admin_hash.py # Admin setup
│   ├── migrations/                # Alembic migrations
│   ├── config.py                  # Multi-environment config
│   ├── run.py                     # Application entry point
│   └── README.md
│
├── part4/                          # Phase 4: Frontend
│   ├── index.html                 # Places listing
│   ├── login.html                 # Authentication
│   ├── place.html                 # Place details
│   ├── add_review.html            # Review submission
│   ├── styles.css                 # Global styles
│   ├── scripts.js                 # Frontend logic
│   ├── images/                    # Assets
│   └── README.md
│
└── README.md                       
```

---


### Complete Setup (Parts 3 & 4)

#### 1. Clone the Repository
```bash
git clone https://github.com/linawsm52/holbertonschool-hbnb/tree/main
cd holbertonschool-hbnb
```

#### 2. Backend Setup (Part 3)

```bash
# Navigate to part3
cd part3

# Create virtual environment
python3 -m venv venv
source venv/bin/activate 

# Install dependencies
pip install -r requirements.txt

# Create MySQL database
mysql -u root -p
```

In MySQL:
```sql
CREATE DATABASE hbnb_db;
USE hbnb_db;
SOURCE sql/schema.sql;
SOURCE sql/data.sql;
EXIT;
```

```bash
# Generate admin password hash
python3 sql/generate_admin_hash.py

# Create admin user
mysql -u root -p hbnb_db < sql/create_admin.sql

# Run the backend
python3 run.py
```

Backend will run at: `http://127.0.0.1:5000`

#### 3. Frontend Setup (Part 4)

```bash
# Open new terminal
cd part4

# Start frontend server
python3 -m http.server 8000
```

Frontend will run at: `http://localhost:8000`

---


## Authors
- Lina Alduaylij — [@linawsm52](https://github.com/linawsm52)
- Ghaida Almutairi — [@GhaidaAl36](https://github.com/GhaidaAl36)
- Alanoud Naif - [@alanooud1983-bot](https://github.com/alanooud1983-bot)
