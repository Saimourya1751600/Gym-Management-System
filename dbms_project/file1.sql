CREATE DATABASE gym_aero_yoga_zumba_management;
USE gym_aero_yoga_zumba_management;

-- Login Table
CREATE TABLE Login (
    Login_ID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) NOT NULL,
    Password VARCHAR(50) NOT NULL
);

-- Client Table
CREATE TABLE Client (
    Client_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Contact VARCHAR(15) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Login_ID INT,
    FOREIGN KEY (Login_ID) REFERENCES Login(Login_ID) ON DELETE CASCADE
);

-- Trainer Table
CREATE TABLE Trainer (
    Trainer_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Expertise VARCHAR(100) NOT NULL,
    Contact VARCHAR(15) NOT NULL,
    password varchar(20) NOt NULL,
    Login_ID INT,
    FOREIGN KEY (Login_ID) REFERENCES Login(Login_ID) ON DELETE CASCADE
);

-- Membership Table
CREATE TABLE Membership (
    Membership_ID INT PRIMARY KEY AUTO_INCREMENT,
    Type VARCHAR(50) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    Client_ID INT,
    FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID) ON DELETE CASCADE
);

-- Payment Table
CREATE TABLE Payment (
    Payment_ID INT PRIMARY KEY AUTO_INCREMENT,
    Amount DECIMAL(10, 2) NOT NULL,
    Date DATE NOT NULL,
    Client_ID INT,
    UPI_ID varchar(30),
    FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID) ON DELETE CASCADE
);

-- Transaction_Record Table
CREATE TABLE Transaction_Record (
    Transaction_ID INT PRIMARY KEY AUTO_INCREMENT,
    Description VARCHAR(255) NOT NULL,
    Date DATE NOT NULL,
    Payment_ID INT,
    
    
    FOREIGN KEY (Payment_ID) REFERENCES Payment(Payment_ID) ON DELETE CASCADE
    
);



-- Schedule Table
CREATE TABLE Schedule (
    Schedule_ID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATE NOT NULL,
    Time TIME NOT NULL
);

-- Workout_Type Table
CREATE TABLE Workout_Type (
    Workout_Type_ID INT PRIMARY KEY AUTO_INCREMENT,
    Type VARCHAR(50) NOT NULL
);

-- Trainer_Schedule Junction Table (Many-to-Many Relationship)
CREATE TABLE Trainer_Schedule (
    Trainer_ID INT,
    Schedule_ID INT,
    PRIMARY KEY (Trainer_ID, Schedule_ID),
    FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID) ON DELETE CASCADE,
    FOREIGN KEY (Schedule_ID) REFERENCES Schedule(Schedule_ID) ON DELETE CASCADE
);

-- Client_Schedule Junction Table (Many-to-Many Relationship)
CREATE TABLE Client_Schedule (
    Client_ID INT,
    Schedule_ID INT,
    PRIMARY KEY (Client_ID, Schedule_ID),
    FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID) ON DELETE CASCADE,
    FOREIGN KEY (Schedule_ID) REFERENCES Schedule(Schedule_ID) ON DELETE CASCADE
);

-- Client_Workout_Type Junction Table (Many-to-Many Relationship)
CREATE TABLE Client_Workout_Type (
    Client_ID INT,
    Workout_Type_ID INT,
    PRIMARY KEY (Client_ID, Workout_Type_ID),
    FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID) ON DELETE CASCADE,
    FOREIGN KEY (Workout_Type_ID) REFERENCES Workout_Type(Workout_Type_ID) ON DELETE CASCADE
);

-- Trainer_Workout_Type Junction Table (Many-to-Many Relationship)
CREATE TABLE Trainer_Workout_Type (
    Trainer_ID INT,
    Workout_Type_ID INT,
    PRIMARY KEY (Trainer_ID, Workout_Type_ID),
    FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID) ON DELETE CASCADE,
    FOREIGN KEY (Workout_Type_ID) REFERENCES Workout_Type(Workout_Type_ID) ON DELETE CASCADE
);

ALTER TABLE Login
ADD CONSTRAINT unique_username UNIQUE (Username);
CREATE TABLE Audit_Log (
    Audit_ID INT AUTO_INCREMENT PRIMARY KEY,
    Action VARCHAR(50),
    Table_Name VARCHAR(50),
    DEL_NAME VARCHAR(50),
    Record_ID INT,
    Action_Time DATETIME
);



DELIMITER $$

CREATE TRIGGER after_client_delete
AFTER DELETE ON Client
FOR EACH ROW
BEGIN
   -- Insert debug information to track if the trigger is firing
   INSERT INTO Audit_Log (Action, Table_Name, Record_ID, Action_Time, DEL_NAME)
   VALUES ('DELETE', 'Client', OLD.Client_ID, NOW(), OLD.Name);
   
   -- Add more debug information if needed
   INSERT INTO Audit_Log (Action, Table_Name, Record_ID, Action_Time, DEL_NAME)
   VALUES ('DEBUG', 'Client_Delete_Trigger', NULL, NOW(), 'Trigger Fired');
END $$

DELIMITER ;



