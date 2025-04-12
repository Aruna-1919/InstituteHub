CREATE DATABASE IF NOT EXISTS institutehub;
USE institutehub;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    role ENUM('admin', 'faculty', 'student')
);

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    date DATE,
    created_by INT,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    posted_by INT,
    FOREIGN KEY (posted_by) REFERENCES users(id)
);

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    date DATE,
    category VARCHAR(50),  -- 'Tech', 'Cultural', 'Sports'
    created_by varchar(100),
    description TEXT
);

CREATE TABLE tech_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    event_id INT,
    stu_name varchar(40),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE cultural_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    event_id INT,
    stu_name varchar(40),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE sports_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    event_id INT,
    stu_name varchar(40),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    assigned_by varchar(100),
    description TEXT
);
ALTER TABLE events
DROP COLUMN created_by;
