-- Run this in MySQL to create your tables
USE CarReservationSystem;

CREATE TABLE Cars (
    Id int PRIMARY KEY,
    Brand varchar(100),
    Model varchar(100),
    Year int,
    PricePerDay decimal(10,2),
    Electric boolean,
    LicensePlate varchar(20)
);

CREATE TABLE CarReservations (
    Id int PRIMARY KEY AUTO_INCREMENT,
    CarId int,
    CustomerName varchar(100),
    Duration int,
    Cost decimal(10,2),
    ElectricRequired boolean,
    FOREIGN KEY (CarId) REFERENCES Cars(Id)
);