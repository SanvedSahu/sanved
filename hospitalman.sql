CREATE DATABASE hospital_db;
create database if not exists hospital_db;Appointments
USE hospital_db;

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('super_admin', 'doctor') NOT NULL
);

CREATE TABLE Patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender ENUM('Male', 'Female', 'Other'),
    phone VARCHAR(15) UNIQUE,
    address TEXT,
    illness VARCHAR(255)
);

CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE,  -- Foreign Key from Users Table
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    phone VARCHAR(15) UNIQUE,
    email VARCHAR(100) UNIQUE,
    available_days TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Appointments (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

INSERT INTO Users (username, password, role) VALUES ('admin', 'adminpass', 'super_admin');

INSERT INTO Users (username, password, role) VALUES ('doc123', 'docpass', 'doctor');

INSERT INTO Doctors (user_id, name, specialization, phone, email, available_days)
VALUES (LAST_INSERT_ID(), 'Dr. Smith', 'Cardiology', '9876543210', 'drsmith@email.com', 'Mon, Wed, Fri');

INSERT INTO Patients (name, age, gender, phone, address, illness)
VALUES ('Alice', 28, 'Female', '9876543211', '45 Street, City', 'Cardiology');

INSERT INTO Appointments (patient_id, doctor_id, appointment_date, appointment_time, status)
VALUES (1, 1, '2025-02-05', '10:30:00', 'Scheduled');

SELECT * FROM Doctors;
SELECT * FROM Patients;
SELECT * FROM Appointments;

SELECT username, password FROM Users;

UPDATE Users SET password = '$2b$12$1caVen16MfrZvisAnnyg5.E/6obYwkVPCHGU5CTTRrLGol/WHs9y6' WHERE username = 'admin';
UPDATE Users SET password = '$2b$12$OHPnzsdPvj1daukacPtrw.NLjaLfd9Jzw23IlrdPLTHWh5lqrQmRC' WHERE username = 'doc123';
