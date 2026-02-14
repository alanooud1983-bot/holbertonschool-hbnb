-- First, delete the existing admin user if it exists
DELETE FROM users WHERE email = 'admin@hbnb.io';

-- Insert admin user with properly formatted bcrypt hash
-- Password: admin1234
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$mN.I73sbj.R72OGyiXQe4uzLVM0Y7maO6TmoHmjbrLDqydZ6Gyruu',  -- bcrypt hash of 'admin1234'
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Verify the insert
SELECT id, first_name, last_name, email, is_admin FROM users WHERE email = 'admin@hbnb.io';