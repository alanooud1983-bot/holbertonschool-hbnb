# Setup Guide

### Configure MySQL (Reset Root Password if Needed)

```bash
sudo mkdir -p /var/run/mysqld
sudo chown mysql:mysql /var/run/mysqld
sudo mysqld_safe --skip-grant-tables &
mysql -u root
```

In MySQL prompt:

```sql
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'password123';
EXIT;
```

### Restart MySQL:

```bash
sudo pkill mysqld
sudo systemctl start mysql
```

### Clone the Repository & Setup Virtual Environment

```bash
git clone https://github.com/linawsm52/holbertonschool-hbnb/tree/a3469970b6495676323b37f3b161b062369cdd5d
cd holbertonschool-hbnb/part3

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Make sure MySQL is running:

```bash
sudo systemctl start mysql
sudo systemctl status mysql
```

### Create Database

```bash
mysql -u root -p
```

In MySQL prompt:
```sql
CREATE DATABASE hbnb_db;
EXIT;
```

### Load Database Schema and Initial Data
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

Verify data:

```bash
mysql -u root -p
```

In MySQL prompt:
```sql
USE hbnb_db;
SHOW TABLES;
SELECT id, email, is_admin FROM users;
```

### run the app

```bash
python3 run.py
```

* login as admin

```bash
curl -X POST http://localhost:5000/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hbnb.io",
    "password": "admin1234"
  }'
```

```
export admin_token="PASTE_THE_TOKEN_HERE"
```

Test protected endpoint:

```bash
curl -X GET http://127.0.0.1:5000/api/v1/protected \
  -H "Authorization: Bearer $admin_token"
```

## Users

* Create User

```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $admin_token" \
  -d '{"first_name":"John",
      "last_name":"Doe",
      "email":"john@example.com",
      "password":"userpass123"
      }'
```

* User Login

```bash
curl -X POST http://127.0.0.1:5000/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "userpass123"
  }'
```

* Get User by ID

```bash
curl -X GET http://localhost:5000/api/v1/users/{user_id} \
  -H "Authorization: Bearer $admin_token"
```

* Get All Users

```bash
curl -X GET http://localhost:5000/api/v1/users/ \
  -H "Authorization: Bearer $admin_token"
```

* Update User (By User)

```bash
curl -X PUT http://localhost:5000/api/v1/users/{user_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $user_token" \
  -d '{
    "first_name": "Johnny",
    "last_name": "Doe"
  }'
```

* Update User (By Admin)

```bash
curl -X PUT http://localhost:5000/api/v1/users/{user_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $admin_token" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@example.com"
  }'
```

## Places

* Create Place

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $admin_token" \
  -d '{
    "title": "Beach House",
    "description": "Beautiful house near the beach",
    "price": 120.00,
    "latitude": 34.05,
    "longitude": -118.25,
    "owner_id": "{owner_id}"
  }'
```

* Get Place by ID

```bash
curl http://127.0.0.1:5000/api/v1/places/{place_id}
```

* Get All Places

```bash
curl http://127.0.0.1:5000/api/v1/places/
```

* Update Place (Admin or Owner)

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/places/{place_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $admin_token" \
  -d '{
    "title": "Updated Beach House",
    "description": "Newly renovated beach house with modern amenities",
    "price": 180.00
  }'
```

* Delete Place (Admin or Owner)

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/places/{place_id} \
  -H "Authorization: Bearer $admin_token"
```

## Amenities

* Create Amenity

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $admin_token" \
  -d '{"name": "WiFi"}'
```

* Get Amenity by ID

```bash
curl -X GET http://127.0.0.1:5000/api/v1/amenities/{amenity_id}
```

* Get All Amenities

```bash
curl -X GET http://127.0.0.1:5000/api/v1/amenities/
```

* Update Amenity

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/{amenity_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $admin_token" \
  -d '{"name": "High-Speed WiFi"}'
```

* Delete Amenity

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/amenities/{amenity_id} \
  -H "Authorization: Bearer $admin_token"
```

* Add Amenity to Place

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/{place_id}/amenities/{amenity_id} \
  -H "Authorization: Bearer $admin_token"
```

* Remove Amenity from Place

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/places/{place_id}/amenities/{amenity_id} \
  -H "Authorization: Bearer $admin_token"
```

## Reviews

* Add Review

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/{place_id}/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $user_token" \
  -d '{
    "text": "Absolutely perfect! The view was stunning and the amenities were top-notch.",
    "rating": 5
  }'
```

* Get Reviews by Place

```bash
curl http://127.0.0.1:5000/api/v1/places/{place_id}/reviews
```

* Get Review by ID

```bash
curl http://127.0.0.1:5000/api/v1/reviews/{review_id}
```

* Update Review (Admin or Owner)

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/reviews/{review_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $user_token" \
  -d '{
    "text": "Updated review: Even better on second visit!",
    "rating": 5
  }'
```

* Delete Review (Admin or Owner)

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/{review_id} \
  -H "Authorization: Bearer $user_token"
```


### sql commands

* Show Tables

```sql
SHOW TABLES;
```

* see table 

```sql
SHOW COLUMNS FROM users;
# or
DESCRIBE users;
```

* view data

```sql
SELECT * FROM users;
```

* Show Specific Columns

```sql
SELECT first_name, email FROM users;
```

* check admin

```sql
SELECT * FROM users WHERE is_admin = 1;
```

* count rows

```sql
SELECT COUNT(*) FROM users;
```

### Common Commands

```bash
# Create migration
flask db migrate -m "description"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade

# Generate admin hash
python3 sql/generate_admin_hash.py

# Access MySQL
mysql -u root -p hbnb_db

# Run tests
python -m pytest app/unit_test/
```
