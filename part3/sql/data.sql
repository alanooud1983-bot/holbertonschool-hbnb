SELECT 'Users:' AS Table_Name;
SELECT id, first_name, last_name, email, is_admin FROM users;

SELECT 'Amenities:' AS Table_Name;
SELECT id, name FROM amenities;


SELECT 
    (SELECT COUNT(*) FROM users) AS total_users,
    (SELECT COUNT(*) FROM amenities) AS total_amenities;