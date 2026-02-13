#!/usr/bin/env python3
"""
Generate bcrypt hash for admin password
Usage: python generate_admin_hash.py
"""

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Password to hash
password = "admin1234"

# Generate hash
hashed = bcrypt.generate_password_hash(password).decode('utf-8')

print("=" * 60)
print("Admin Password Hash Generator")
print("=" * 60)
print(f"Original Password: {password}")
print(f"Bcrypt Hash: {hashed}")
print("=" * 60)
print("\nUse this hash in your data.sql file!")
