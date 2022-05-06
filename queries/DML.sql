-- Query for insertion of a new Attendee in Attendees
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Attendees (name_prefix ,first_name, last_name, name_suffix)
VALUES (:name_prefix_input, :first_name_input, :last_name_input, :name_suffix_input);

-- Query for getting the full name of all Attendees
-- Colon denotes variable that will be obtained through form submission or specific table row
SELECT attendee_id, full_name
FROM Attendees;

-- Query for updating the rows in Attendees that have the first set of passed-in values to have the second set of passed-in values
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Attendees
SET name_prefix = :name_prefix_input, 
first_name = :first_name_input, 
last_name = :last_name_input,
name_suffix = :name_suffix_input
WHERE name_prefix = :old_name_prefix_input
AND first_name = :old_first_name_input
AND last_name = :old_last_name_input
AND name_suffix = :old_name_suffix_input;

-- Query for updating the entry in Attendees with the matching attendee_id
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Attendees
SET name_prefix = :name_prefix_input, 
first_name = :first_name_input, 
last_name = :last_name_input,
name_suffix = :name_suffix_input
WHERE attendee_id = :id_input;

-- Query for deleting the matching rows from the Attendee table
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Attendees
WHERE name_prefix = :name_prefix_input
AND first_name = :first_name_input
AND last_name = :last_name_input
AND name_suffix = :name_suffix_input;

-- Query for deleting the entry in Attendees with the matching attendee_id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Attendees
WHERE attendee_id = :id_input



-- Query for insertion of a new Spirit in Spirits
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Spirits (name_prefix ,first_name, last_name, name_suffix)
VALUES (:name_prefix_input, :first_name_input, :last_name_input, :name_suffix_input);

-- Query for getting the full name of all Spirits
-- Colon denotes variable that will be obtained through form submission or specific table row
SELECT spirit_id, full_name
FROM Spirits;

-- Query for updating the rows in Spirits that have the first set of passed-in values to have the second set of passed-in values
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Spirits
SET name_prefix = :name_prefix_input, 
first_name = :first_name_input, 
last_name = :last_name_input,
name_suffix = :name_suffix_input
WHERE name_prefix = :old_name_prefix_input
AND first_name = :old_first_name_input
AND last_name = :old_last_name_input
AND name_suffix = :old_name_suffix_input;

-- Query for updating the entry in Spirits with the matching spirit_id
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Spirits
SET name_prefix = :name_prefix_input, 
first_name = :first_name_input, 
last_name = :last_name_input,
name_suffix = :name_suffix_input
WHERE spirit_id = :id_input;


-- Query for deleting the matching rows from the Spirit table
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Spirits
WHERE name_prefix = :name_prefix_input
AND first_name = :first_name_input
AND last_name = :last_name_input
AND name_suffix = :name_suffix_input;

-- Query for deleting the entry in Spirits with the matching spirit_id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Spirits
WHERE spirit_id = :id_input

-- Query for insertion of a new Medium in Mediums
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Mediums (name_prefix ,first_name, last_name, name_suffix)
VALUES (:name_prefix_input, :first_name_input, :last_name_input, :name_suffix_input);

-- Query for getting the id and full name of all Mediums
-- Colon denotes variable that will be obtained through form submission or specific table row
SELECT medium_id, full_name
FROM Mediums;

-- Query for updating the rows in Mediums that have the first set of passed-in values to have the second set of passed-in values
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Mediums
SET name_prefix = :name_prefix_input, 
first_name = :first_name_input, 
last_name = :last_name_input,
name_suffix = :name_suffix_input
WHERE name_prefix = :old_name_prefix_input
AND first_name = :old_first_name_input
AND last_name = :old_last_name_input
AND name_suffix = :old_name_suffix_input;

-- Query for updating the entry in Mediums with the matching medium_id
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Mediums
SET name_prefix = :name_prefix_input, 
first_name = :first_name_input, 
last_name = :last_name_input,
name_suffix = :name_suffix_input
WHERE medium_id = :id_input;

-- Query for deleting the matching rows from the Medium table
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Mediums
WHERE name_prefix = :name_prefix_input
AND first_name = :first_name_input
AND last_name = :last_name_input
AND name_suffix = :name_suffix_input;

-- Query for deleting the medium with the passed-in id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Mediums
WHERE medium_id = :id_input;


-- Query for creating a new Location
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Locations (name, street_address, city, zip, state, country)
VALUES (:name_input, :street_address_input, :city_input, :zip_input, :state_input, :country_input);

-- Query for getting the full list of Locations
-- Colon denotes variable that will be obtained through form submission or specific table row
SELECT location_id, name, street_address, city, zip, state, country
FROM Locations;

-- Query for updating the Locations that have the first set of passed-in values to have the second set of passed-in values
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Locations
SET name = :name_input,
street_address = :street_address_input,
city = :city_input, 
zip = :zip_input,
state = :state_input,
country = :country_input
WHERE name = :old_name_input
AND street_address = :old_street_address_input
AND city = :old_city_input 
AND zip = :old_zip_input
AND state = :old_state_input
AND country = :old_country_input;

-- Query for updating the Location with the passed-in id
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Locations
SET name = :name_input,
street_address = :street_address_input,
city = :city_input, 
zip = :zip_input,
state = :state_input,
country = :country_input
WHERE location_id = :id_input;

-- Query for deleting the Locations that match the query
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Locations
WHERE name = :name_input
AND street_address = :old_street_address_input
AND city = :old_city_input 
AND zip = :old_zip_input
AND state = :old_state_input
AND country = :old_country_input;

-- Query for deleting the Location with the passed-in id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Locations
WHERE location_id = :id_input;

-- Query for creating a new Seance
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Seances (date, location_id)
VALUES (
    :date_input, 
    (SELECT location_id 
     FROM Locations
     WHERE name = :location_name_input
    );

-- Query for getting the full list of Seances with location name
-- Colon denotes variable that will be obtained through form submission or specific table row
SELECT Seances.seance_id, Locations.name, Seances.date
FROM Seances
INNER JOIN Locations ON Seances.location_id = Locations.location_id;

-- Query for updating a Seance
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Seances
SET date = :date_input,
location_id = (SELECT location_id 
               FROM Locations
               WHERE name = :location_name_input)
WHERE date = :old_date_input
AND location_id = (SELECT location_id
                   FROM Locations
                   WHERE name = :old_location_name_input);
            
-- Query for updating a Seance based on its id
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Seances
SET date = :date_input,
location_id = (SELECT location_id 
               FROM Locations
               WHERE name = :location_name_input)
WHERE seance_id = :id_input;

-- Query for deleting a Seance
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Seances
WHERE date = :date_input
AND location_id = (SELECT location_id
                   FROM Locations
                   WHERE name = :location_name_input);
            
-- Query for deleting the Seance with the passed-in id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Seances
WHERE seance_id = :id_input;


-- Query for adding a Method
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Methods (name, description)
VALUES (:name_input, :name_description);

-- Query for getting the full list of methods
-- Colon denotes variable that will be obtained through form submission or specific table row
SELECT method_id, name, description
FROM Methods;

-- Query for updating a method based on name
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Methods
SET name = :name_input,
description = :description_input
WHERE name = :old_name_input;

-- Query for updating a method based on id
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Methods
SET name = :name_input,
description = :description_input
WHERE method_id = :id_input;

-- Query for deleting a method based on name
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Methods
WHERE name = :name_input;

-- Query for deleteing a method based on id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Methods
WHERE method_id = :id_input;

-- Query for adding a Channeling
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Channelings (medium_id, seance_id, spirit_id, method_id, is_successful, length_in_minutes)
VALUES 
(
(
SELECT medium_id
FROM Mediums
WHERE full_name = :medium_full_name_input
),
(SELECT Seances.seance_id
 FROM Seances
 INNER JOIN Locations ON Seances.location_id = Locations.location_id
 WHERE Locations.name = :location_name_input
 AND Seances.date = :date_input),
 (SELECT spirit_id
 FROM Spirits
 WHERE full_name = :spirit_full_name_input),
 (SELECT method_id
 FROM Methods
 WHERE name = :method_name_input),
 :is_successful_input,
 :length_in_minutes_input
);

-- Query for displaying all Channelings with Medium name, Spirit name, Method name, date, and stats
-- Colon denotes variable that will be obtained through form submission or specific table row
SELECT Mediums.full_name, Spirits.full_name, Methods.name, Seances.date, Locations.name, Channelings.is_successful, Channelings.length_in_minutes
FROM Channelings
INNER JOIN Mediums ON Channelings.medium_id = Mediums.medium_id
INNER JOIN Spirits ON Channelings.spirit_id = Spirits.spirit_id
INNER JOIN Methods ON Channelings.method_id = Methods.method_id
INNER JOIN Seances ON Channelings.seance_id = Seances.seance_id
INNER JOIN Locations ON Seances.location_id = Locations.location_id;

-- Query for updating a Channeling
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Channelings
SET medium_id = (SELECT medium_id
                 FROM Mediums
                 WHERE full_name = :medium_full_name_input),
    seance_id = (SELECT Seances.seance_id
                 FROM Seances
                 INNER JOIN Locations ON Seances.location_id = Locations.location_id
                 WHERE Locations.name = :location_name_input
                 AND Seances.date = :date_input),
    spirit_id = (SELECT spirit_id
                 FROM Spirits
                 WHERE full_name = :spirit_full_name_input),
    method_id = (SELECT method_id
                 FROM Methods
                 WHERE name = :method_name_input),
    is_successful = :is_successful_input,
    length_in_minutes = :length_in_minutes_input
WHERE medium_id = (SELECT medium_id
                 FROM Mediums
                 WHERE full_name = old_medium_full_name_input)
AND seance_id = (SELECT Seances.seance_id
                 FROM Seances
                 INNER JOIN Locations ON Seances.location_id = Locations.location_id
                 WHERE Locations.name = :old_location_name_input
                 AND Seances.date = :old_date_input)
AND spirit_id = (SELECT spirit_id
                 FROM Spirits
                 WHERE full_name = :old_spirit_full_name_input)
AND method_id = (SELECT method_id
                 FROM Methods
                 WHERE name = :old_method_name_input)
AND is_successful = :old_is_successful_input
AND length_in_minutes = :old_length_in_minutes_input;

 -- Query for updating a Channeling based on id
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Channelings
SET medium_id = (SELECT medium_id
                 FROM Mediums
                 WHERE full_name = :medium_full_name_input),
    seance_id = (SELECT Seances.seance_id
                 FROM Seances
                 INNER JOIN Locations ON Seances.location_id = Locations.location_id
                 WHERE Locations.name = :location_name_input
                 AND Seances.date = :date_input),
    spirit_id = (SELECT spirit_id
                 FROM Spirits
                 WHERE full_name = :spirit_full_name_input),
    method_id = (SELECT method_id
                 FROM Methods
                 WHERE name = :method_name_input),
    is_successful = :is_successful_input,
    length_in_minutes = :length_in_minutes_input
WHERE channeling_id = :id_input;

-- Query for deleting a Channeling
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Channelings
WHERE medium_id = (SELECT medium_id
                 FROM Mediums
                 WHERE full_name = :old_medium_full_name_input)
AND seance_id = (SELECT Seances.seance_id
                 FROM Seances
                 INNER JOIN Locations ON Seances.location_id = Locations.location_id
                 WHERE Locations.name = :old_location_name_input
                 AND Seances.date = :old_date_input)
AND spirit_id = (SELECT spirit_id
                 FROM Spirits
                 WHERE full_name = :old_spirit_full_name_input)
AND method_id = (SELECT method_id
                 FROM Methods
                 WHERE name = :old_method_name_input)
AND is_successful = :old_is_successful_input
AND length_in_minutes = :old_length_in_minutes_input;
 
-- Query for deleting a Channeling based on id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Channelings
WHERE channeling_id = id_input;

-- Query for inserting a record of an Attendee attending a Seance
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO SeanceAttendees (attendee_id, seance_id)
VALUES 
(
    (SELECT Attendees.attendee_id
     FROM Attendees
     WHERE Attendees.full_name = :attendee_full_name_input),
    (SELECT Seances.seance_id
     FROM Seances
     INNER JOIN Locations on Seances.location_id = Locations.location_id
     WHERE Seances.date = :date_input
     AND Locations.name = :location_name_input)
);

-- Query for getting a list of names and ids of all Attendees of a Seance
-- Colon denotes variable that will be obtained through form submission or specific table row
SELECT Attendees.attendee_id, Attendees.full_name
FROM Seances
INNER JOIN SeanceAttendees ON Seances.seance_id = SeanceAttendees.seance_id
INNER JOIN Attendees ON SeanceAttendees.attendee_id = Attendees.attendee_id
INNER JOIN Locations ON Seances.location_id = Locations.location_id
WHERE Seances.date = :date_input
AND Locations.name = :location_name_input;

-- Query for getting a list of Seance ids, dates, and locations for all Seances attended by one Attendee
-- Colon denotes variable that will be obtained through form submission or specific table row
SELECT Seances.seance_id, Seances.date, Locations.location_id, Locations.name
FROM Attendees
INNER JOIN SeanceAttendees ON Attendees.attendee_id = SeanceAttendees.attendee_id
INNER JOIN Seances ON SeanceAttendees.seance_id = Seances.seance_id
INNER JOIN Locations ON Seances.location_id = Locations.location_id
WHERE Attendees.full_name = :attendee_full_name_input;


-- Query for deleting a record of a Seance being attended by an Attendee
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM SeanceAttendees
WHERE attendee_id = (SELECT attendee_id
                     FROM Attendees
                     WHERE attendee.full_name = :old_attendee_full_name_input)
AND seance_id = (SELECT seance_id
                 FROM Seances
                 INNER JOIN Locations ON Seances.location_id = Locations.location_id
                 WHERE Location.name = :old_location_name_input
                 AND Seances.date = :old_date_input);
 
