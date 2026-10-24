CREATE DATABASE IF NOT EXISTS `food_surplus_db`;
USE `food_surplus_db`;

DROP VIEW IF EXISTS `deliverysummary`;
DROP TABLE IF EXISTS `REDISTRIBUTION`;
DROP TABLE IF EXISTS `DONATION`;
DROP TABLE IF EXISTS `VOLUNTEER`;
DROP TABLE IF EXISTS `RECIPIENT`;
DROP TABLE IF EXISTS `FOOD_CATEGORY`;
DROP TABLE IF EXISTS `DONOR`;

CREATE TABLE `DONOR` (
  `DonorID` int NOT NULL AUTO_INCREMENT,
  `DonorName` varchar(100) NOT NULL,
  `DonorType` varchar(50) DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  `City` varchar(50) DEFAULT NULL,
  `Pincode` varchar(10) DEFAULT NULL,
  `RegDate` date DEFAULT NULL,
  `Status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`DonorID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `FOOD_CATEGORY` (
  `CategoryID` int NOT NULL AUTO_INCREMENT,
  `CategoryName` varchar(50) NOT NULL,
  `StorageRequirement` varchar(100) DEFAULT NULL,
  `ShelfLifeHours` int DEFAULT NULL,
  PRIMARY KEY (`CategoryID`),
  UNIQUE KEY `CategoryName` (`CategoryName`),
  CONSTRAINT `food_category_chk_1` CHECK ((`ShelfLifeHours` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `RECIPIENT` (
  `RecipientID` int NOT NULL AUTO_INCREMENT,
  `RecipientName` varchar(100) NOT NULL,
  `RecipientType` varchar(50) DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  `City` varchar(50) DEFAULT NULL,
  `CapacityKg` decimal(10,2) DEFAULT NULL,
  `ContactPerson` varchar(100) DEFAULT NULL,
  `RegDate` date DEFAULT NULL,
  `Status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`RecipientID`),
  UNIQUE KEY `Email` (`Email`),
  CONSTRAINT `recipient_chk_1` CHECK ((`CapacityKg` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `VOLUNTEER` (
  `VolunteerID` int NOT NULL AUTO_INCREMENT,
  `VolunteerName` varchar(100) NOT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `OperatingZone` varchar(100) DEFAULT NULL,
  `AvailabilityStatus` varchar(30) DEFAULT NULL,
  `VehicleType` varchar(50) DEFAULT NULL,
  `VehicleCapacityKg` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`VolunteerID`),
  UNIQUE KEY `Email` (`Email`),
  CONSTRAINT `volunteer_chk_1` CHECK ((`VehicleCapacityKg` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `DONATION` (
  `DonationID` int NOT NULL AUTO_INCREMENT,
  `DonorID` int NOT NULL,
  `CategoryID` int NOT NULL,
  `FoodName` varchar(100) NOT NULL,
  `Quantity` decimal(10,2) DEFAULT NULL,
  `Unit` varchar(20) DEFAULT NULL,
  `ListingDateTime` datetime DEFAULT NULL,
  `ExpiryDateTime` datetime DEFAULT NULL,
  `PrepDateTime` datetime DEFAULT NULL,
  `PickupAddress` varchar(200) DEFAULT NULL,
  `Status` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`DonationID`),
  KEY `DonorID` (`DonorID`),
  KEY `CategoryID` (`CategoryID`),
  CONSTRAINT `donation_ibfk_1` FOREIGN KEY (`DonorID`) REFERENCES `DONOR` (`DonorID`),
  CONSTRAINT `donation_ibfk_2` FOREIGN KEY (`CategoryID`) REFERENCES `FOOD_CATEGORY` (`CategoryID`),
  CONSTRAINT `donation_chk_1` CHECK ((`Quantity` > 0)),
  CONSTRAINT `donation_chk_2` CHECK (((`ExpiryDateTime` is null) or (`ListingDateTime` is null) or (`ExpiryDateTime` > `ListingDateTime`)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `REDISTRIBUTION` (
  `RedistribID` int NOT NULL AUTO_INCREMENT,
  `DonationID` int NOT NULL,
  `RecipientID` int NOT NULL,
  `VolunteerID` int DEFAULT NULL,
  `QuantityAllocated` decimal(10,2) DEFAULT NULL,
  `MatchDateTime` datetime DEFAULT NULL,
  `DispatchDateTime` datetime DEFAULT NULL,
  `DeliveryDateTime` datetime DEFAULT NULL,
  `DeliveryStatus` varchar(30) DEFAULT NULL,
  `FeedbackRating` int DEFAULT NULL,
  `FeedbackComments` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`RedistribID`),
  KEY `DonationID` (`DonationID`),
  KEY `RecipientID` (`RecipientID`),
  KEY `VolunteerID` (`VolunteerID`),
  CONSTRAINT `redistribution_ibfk_1` FOREIGN KEY (`DonationID`) REFERENCES `DONATION` (`DonationID`),
  CONSTRAINT `redistribution_ibfk_2` FOREIGN KEY (`RecipientID`) REFERENCES `RECIPIENT` (`RecipientID`),
  CONSTRAINT `redistribution_ibfk_3` FOREIGN KEY (`VolunteerID`) REFERENCES `VOLUNTEER` (`VolunteerID`),
  CONSTRAINT `redistribution_chk_1` CHECK ((`QuantityAllocated` > 0)),
  CONSTRAINT `redistribution_chk_2` CHECK ((`FeedbackRating` between 1 and 5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `DONOR` VALUES (1,'Fresh Mart','Supermarket','9876543210','fresh@demo.com','Anna Nagar','Chennai','600040','2026-01-10','Active'),(2,'Green Hotel','Hotel','9876543211','green@demo.com','T Nagar','Chennai','600017','2026-01-12','Active'),(3,'Sunrise Bakery','Bakery','9876543212','sunrise@demo.com','Velachery','Chennai','600042','2026-02-01','Active'),(4,'City Restaurant','Restaurant','9876543213','city@demo.com','OMR','Chennai','600096','2026-02-15','Active'),(5,'Daily Needs Store','Supermarket','9876543214','daily@demo.com','Porur','Chennai','600116','2026-03-01','Active');

INSERT INTO `FOOD_CATEGORY` VALUES (1,'Vegetables','Refrigeration',24),(2,'Cooked Food','Hot or refrigerated storage',8),(3,'Bakery','Dry storage',48),(4,'Dairy Products','Refrigeration',24),(5,'Packaged Food','Dry storage',168);

INSERT INTO `RECIPIENT` VALUES (201,'Helping Hands','NGO','9000000001','help@demo.com','Adyar','Chennai',100.00,'Ravi','2026-01-15','Active'),(202,'Hope Shelter','Shelter','9000000002','hope@demo.com','Guindy','Chennai',80.00,'Priya','2026-02-10','Active'),(203,'Care Centre','NGO','9000000003','care@demo.com','Mylapore','Chennai',60.00,'Arun','2026-03-05','Active'),(204,'Community Kitchen','NGO','9000000004','kitchen@demo.com','Tambaram','Chennai',120.00,'Meena','2026-04-01','Active'),(205,'Hope Orphanage','Orphanage','9000000005','orphanage@demo.com','Porur','Chennai',70.00,'Suresh','2026-04-10','Active');

INSERT INTO `VOLUNTEER` VALUES (301,'Arun Kumar','9000000011','arun@demo.com','North Chennai','Available','Van',100.00),(302,'Priya Devi','9000000012','priya@demo.com','South Chennai','Available','Car',40.00),(303,'Karthik Raj','9000000013','karthik@demo.com','Central Chennai','Busy','Bike',20.00),(304,'Vijay Kumar','9000000014','vijay@demo.com','East Chennai','Available','Van',80.00),(305,'Divya Raj','9000000015','divya@demo.com','West Chennai','Available','Car',35.00);

INSERT INTO `DONATION` VALUES (101,1,1,'Fresh Vegetables',50.00,'kg','2026-10-12 08:00:00','2026-10-13 08:00:00','2026-10-12 06:00:00','Anna Nagar','Available'),(102,2,2,'Cooked Rice',30.00,'kg','2026-10-12 09:00:00','2026-10-12 17:00:00','2026-10-12 07:00:00','T Nagar','Allocated'),(103,3,3,'Bread',20.00,'kg','2026-10-12 10:00:00','2026-10-14 10:00:00','2026-10-12 08:00:00','Velachery','Allocated'),(104,4,2,'Vegetable Meals',40.00,'kg','2026-10-12 11:00:00','2026-10-12 19:00:00','2026-10-12 09:00:00','OMR','Available'),(105,5,5,'Packed Biscuits',25.00,'kg','2026-10-12 12:00:00','2026-10-19 12:00:00','2026-10-12 10:00:00','Porur','Available');

INSERT INTO `REDISTRIBUTION` VALUES (401,102,201,301,20.00,'2026-10-12 09:30:00','2026-10-12 10:00:00','2026-10-12 10:45:00','Delivered',5,'Good condition'),(402,103,202,302,15.00,'2026-10-12 10:30:00','2026-10-12 11:00:00','2026-10-12 11:40:00','Delivered',4,'On time'),(403,102,203,NULL,10.00,'2026-10-12 11:00:00',NULL,NULL,'Pending',NULL,NULL),(404,104,204,304,25.00,'2026-10-12 11:30:00','2026-10-12 12:00:00','2026-10-12 12:45:00','Delivered',5,'Fresh food delivered'),(405,105,205,305,20.00,'2026-10-12 12:30:00','2026-10-12 13:00:00',NULL,'In Transit',NULL,NULL);

CREATE VIEW `deliverysummary` AS
SELECT
    R.`RedistribID`,
    D.`FoodName`,
    C.`RecipientName`,
    R.`QuantityAllocated`,
    R.`DeliveryStatus`
FROM `REDISTRIBUTION` AS R
JOIN `DONATION` AS D ON R.`DonationID` = D.`DonationID`
JOIN `RECIPIENT` AS C ON R.`RecipientID` = C.`RecipientID`;
