SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

DROP TABLE IF EXISTS SeanceAttendees;
DROP TABLE IF EXISTS Channelings;
DROP TABLE IF EXISTS Seances;
DROP TABLE IF EXISTS Methods;
DROP TABLE IF EXISTS Mediums;
DROP TABLE IF EXISTS Attendees;
DROP TABLE IF EXISTS Spirits;

CREATE TABLE Attendees
(
attendee_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY
, full_name VARCHAR(100)
)
;

INSERT INTO Attendees (full_name)
VALUES ('Bess Houdini')
, ( 'Sir Arthur Conan Doyle')
, ('Hilma Klimt')
, ('Alexander Graham Bell')
, ('Maggie Fox')
, ('William T. Stead');


CREATE TABLE Mediums
(
medium_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY
, full_name VARCHAR(100)
)
;

INSERT INTO Mediums (full_name)
VALUES ('Arthur Ford')
, ('Andrew Jackson Davis')
, ('Leah Fox')
, ('Kate Fox')
, ('Maggie Fox')
, ('Edgar Cayce');


CREATE TABLE Spirits
(
spirit_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY
, full_name VARCHAR(100)
)
;

INSERT INTO Spirits (full_name)
VALUES ('Black Hawk')
, ('Harry Houdini')
, ('Batholomew Governor of the House of Strangers')
, ('Benjamin Franklin')
, ('Estelle Livermore');


CREATE TABLE Methods
(
    method_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    name VARCHAR(60),
    description VARCHAR(200)
);

INSERT INTO Methods (name, description)
VALUES 
("Spirit Board", "Medium asks questions of the spirit and the spirit guides their hand over a board of letters and symbols"),
("Cabinets", "Medium is placed into a cabinet and the spirit manipulates objects in the room"),
("Trance", "Medium goes into a trance and delivers messages from the summoned spirit. Medium may or may not remember the messages once they wake.");

DROP TABLE IF EXISTS Locations;

CREATE TABLE Locations
(
location_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY
, name VARCHAR(60)
, street_address VARCHAR(60)
, city VARCHAR(60)
, zip VARCHAR(5)
, state VARCHAR(2)
, country VARCHAR(60) DEFAULT 'US'
)
;

INSERT INTO Locations (name ,street_address, city, zip, state, country)
VALUES ( 'Barnum\'s Hotel','170 Broadway', 'New York','10007' ,'NY',DEFAULT)
, ( 'Beachland Ballroom & Tavern','15711 Waterloo Rd','Cleveland', '44110' ,'OH',DEFAULT)
, ('Hollywood Knickerbocker Hotel','1714 Ivar Ave', 'Hollywood','90028' ,'CA',DEFAULT)
, ('Edgar Cayce\'s - Houston A.R.E. Center','7800 Amelia Road','Houston','77055','TX',DEFAULT)
, ('Alister Hardy Religious Experience Research Centre','College St', 'Lampeter', NULL, NULL,'United Kingdom')
;


CREATE TABLE Seances
(
seance_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
date DATE,
location_id INT,
FOREIGN KEY(location_id) REFERENCES Locations(location_id) ON DELETE SET NULL
)
;

INSERT INTO Seances (date,location_id)
VALUES ( '1943-10-31', (SELECT location_id FROM Locations WHERE name= 'Hollywood Knickerbocker Hotel'))
, ( '1927-04-12', (SELECT location_id FROM Locations WHERE name= 'Alister Hardy Religious Experience Research Centre'))
, ( '1854-03-31', (SELECT location_id FROM Locations WHERE name= "Barnum's Hotel"))
, ( '1920-08-26', (SELECT location_id FROM Locations WHERE name= "Edgar Cayce's - Houston A.R.E. Center"))
, ( '1857-11-21', NULL)
, ( '1857-11-21', (SELECT location_id FROM Locations WHERE name= "Edgar Cayce's - Houston A.R.E. Center"))
;



CREATE TABLE Channelings
(
channeling_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY
, medium_id INT 
, seance_id INT
, spirit_id INT
, method_id INT
, is_successful BOOL DEFAULT 0
, length_in_minutes INT,
FOREIGN KEY(medium_id) REFERENCES Mediums(medium_id) ON DELETE SET NULL,
FOREIGN KEY(seance_id) REFERENCES Seances(seance_id) ON DELETE SET NULL,
FOREIGN KEY(spirit_id) REFERENCES Spirits(spirit_id) ON DELETE SET NULL,
FOREIGN KEY(method_id) REFERENCES Methods(method_id) ON DELETE SET NULL
);

INSERT INTO Channelings (medium_id ,seance_id, spirit_id, method_id, is_successful, length_in_minutes)
VALUES 
(
	(SELECT medium_id FROM Mediums WHERE full_name= 'Arthur Ford')
	, (SELECT seance_id FROM Seances WHERE date= '1943-10-31' 
		AND location_id =(SELECT location_id FROM Locations WHERE name= 'Hollywood Knickerbocker Hotel')) 
	, (SELECT spirit_id FROM Spirits WHERE full_name = ('Harry Houdini'))
	, (SELECT method_id FROM Methods WHERE name = 'Spirit Board')
	, 1
	, 31
)
, (
	(SELECT medium_id FROM Mediums WHERE full_name= 'Kate Fox')
	, (SELECT seance_id FROM Seances WHERE date= '1857-11-21'
		and location_id =(select location_id FROM Locations WHERE Name= 'Beachland Ballroom & Tavern')) 
	, (SELECT spirit_id from Spirits where full_name = ('Black Hawk'))
	, (SELECT method_id from Methods WHERE name = 'Cabinets')
	, 1
	, 17
)
, (
	(SELECT medium_id FROM Mediums WHERE full_name= 'Edgar Cayce')
	, (SELECT seance_id FROM Seances WHERE date= '1920-08-26'
		and location_id =(select location_id FROM Locations WHERE name= "Edgar Cayce's - Houston A.R.E. Center")) 
	, (SELECT spirit_id from Spirits WHERE full_name = ('Benjamin Franklin'))
	, (SELECT method_id from Methods WHERE name = 'Trance')
	, 1
	, 81
),
(
	(SELECT medium_id FROM Mediums WHERE full_name= 'Edgar Cayce')
	, (SELECT seance_id FROM Seances WHERE date= '1857-11-21'
		and location_id =(select location_id FROM Locations WHERE Name= 'Beachland Ballroom & Tavern')) 
	, (SELECT spirit_id from Spirits WHERE full_name = ('Harry Houdini'))
	, (SELECT method_id from Methods WHERE name = 'Trance')
	, 1
	, 81

);

CREATE TABLE SeanceAttendees
(
seanceattendees_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
attendee_id INT,
seance_id INT,
FOREIGN KEY(attendee_id) REFERENCES Attendees(attendee_id) ON DELETE SET NULL,
FOREIGN KEY(seance_id) REFERENCES Seances(seance_id) ON DELETE CASCADE
);

INSERT INTO SeanceAttendees (attendee_id, seance_id)
VALUES 
(
    (SELECT attendee_id FROM Attendees WHERE full_name = 'Sir Arthur Conan Doyle'),
    (SELECT seance_id FROM Seances WHERE date= '1920-08-26'
		AND location_id =(select location_id FROM Locations WHERE name= "Edgar Cayce's - Houston A.R.E. Center"))
),
(
    (SELECT attendee_id FROM Attendees WHERE full_name = 'Hilma Klimt'),
    (SELECT seance_id FROM Seances WHERE date= '1920-08-26'
		AND location_id =(select location_id FROM Locations WHERE name= "Edgar Cayce's - Houston A.R.E. Center"))
),
(
    (SELECT attendee_id FROM Attendees WHERE full_name = 'Maggie Fox'),
    (SELECT seance_id FROM Seances WHERE date = '1857-11-21' 
        AND location_id = (SELECT location_id FROM Locations WHERE name = 'Beachland Ballroom & Tavern'))
),
(
    (SELECT attendee_id FROM Attendees WHERE full_name = 'Maggie Fox'),
    (SELECT seance_id FROM Seances WHERE date= '1920-08-26'
		AND location_id =(select location_id FROM Locations WHERE name= "Edgar Cayce's - Houston A.R.E. Center"))
),
(
    NULL,
    (SELECT seance_id FROM Seances WHERE date=  '1943-10-31'
		AND location_id =(select location_id FROM Locations WHERE name= "Hollywood Knickerbocker Hotel"))
);

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;