CREATE DATABASE IF NOT EXISTS gym_management;
USE gym_management;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_email VARCHAR(100) NOT NULL UNIQUE,
    user_password VARCHAR(255) NOT NULL,
    user_role VARCHAR(50) NOT NULL,
    user_status VARCHAR(50) NOT NULL DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS memberships (
    membership_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    membership_plan VARCHAR(100) NOT NULL,
    membership_price DECIMAL(10, 2) NOT NULL,
    membership_duration INT NOT NULL,
    membership_benefits TEXT,
    membership_status VARCHAR(50) NOT NULL DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    membership_id INT NOT NULL,
    payment_amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_reference VARCHAR(100) NOT NULL,
    payment_status VARCHAR(50) NOT NULL DEFAULT 'paid',
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (membership_id) REFERENCES memberships(membership_id)
);
