-- Create the development database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create the development user
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on the development database
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant SELECT privilege on performance_schema only
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Apply privileges
FLUSH PRIVILEGES;
