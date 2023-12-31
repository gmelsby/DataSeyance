-- Query for insertion of a new Attendee in Attendees
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Attendees (full_name)
VALUES (:full_name_input);

-- Query for insertion of a new Attendee in Attendees that has attended at least one Seance
-- Inserts into SeanceAttendees intersection table as well
-- :seance_id_input to be determined by a dropdown populated by a SELECT query on Seances
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Attendees (full_name)
VALUES (:full_name_input);
SET @new_attendee_id = LAST_INSERT_ID();
-- Perform the following query for all seances the attendee has attended (probably to be implemented using a checkbox)
INSERT INTO SeanceAttendees (attendee_id, seance_id)
VALUES (new_attendee_id, :seance_id_input);

-- Query for getting the full name of all Attendees
-- Also to be used in dropdown to find attendee_id to be added to SeanceAttendee
SELECT attendee_id, full_name
FROM Attendees;

-- Query for pre-populating text box for Update Attendee
-- Colon denotes variable that will be obtained through get query parameters
SELECT attendee_id, full_name
FROM Attendees
WHERE attendee_id = :id_input;

-- Query for updating the entry in Attendees with the matching attendee_id
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Attendees
SET full_name = :full_name_input 
WHERE attendee_id = :id_input;

-- Query for deleting the entry in Attendees with the matching attendee_id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Attendees
WHERE attendee_id = :id_input;



-- Query for insertion of a new Spirit in Spirits
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Spirits (full_name)
VALUES (:full_name_input);

-- Query for getting the full name of all Spirits
-- Also to be used in dropdown to designate Spirit to be updated
-- Also used in dropdown menu for insert Channeling
SELECT spirit_id, full_name
FROM Spirits;

-- Query for getting spirit_id and full name for a Spirit based on spirit_id
-- To be used in dropdown menu preselect for updating a Spirit
-- Colon denotes variable obtained through get request query parameters
SELECT spirit_id, full_name
FROM Spirits
WHERE spirit_id = :id_input;

-- Query for updating the entry in Spirits with the matching spirit_id
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Spirits
SET full_name = :full_name_input 
WHERE spirit_id = :id_input;

-- Query for deleting the entry in Spirits with the matching spirit_id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Spirits
WHERE spirit_id = :id_input;


-- Query for insertion of a new Medium in Mediums
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Mediums (full_name)
VALUES (:full_name_input);

-- Query for getting the id and full name of all Mediums
-- Used for populating dropdown menu for Update Medium
-- Also used in dropdown menu for insert Channeling
SELECT medium_id, full_name
FROM Mediums;

-- Query for getting medium_id and full name for a Medium based on medium_id
-- To be used in dropdown menu preselect for updating a Medium
-- Colon denotes variable obtained through get request query parameters
SELECT medium_id, full_name
FROM Mediums
WHERE  medium_id = :id_input;



-- Query for updating the entry in Mediums with the matching medium_id
-- Also to be used in dropdown to designate Medium to be updated
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Mediums
SET full_name = :full_name_input 
WHERE medium_id = :id_input;

-- Query for deleting the medium with the passed-in id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Mediums
WHERE medium_id = :id_input;


-- Query for creating a new Location
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Locations (name, street_address, city, zip, state, country)
VALUES (:name_input, :street_address_input, :city_input, :zip_input, :state_input, :country_input);

-- Query for getting the full list of Locations
SELECT location_id, name, street_address, city, zip, state, country
FROM Locations;

-- Query for getting a list of Location names with ids
-- Used in drop-down menu for editing and adding Seances
SELECT location_id, name
FROM Locations;

-- Query for getting info about one Location for prefill in Update Location
-- Colon denotes variable obtained through get request parameters
SELECT location_id, name, street_address, city, zip, state, country
FROM Locations
WHERE location_id = :id_input;

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

-- Query for deleting the Location with the passed-in id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Locations
WHERE location_id = :id_input;

-- Query for creating a new Seance
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Seances (date, location_id)
VALUES (
    :date_input, 
    :location_id_input
    );

-- Query for getting the full list of Seances with location name
-- To be displayed on the Seances page
-- Used to populate dropdown and text boxes for Update Seances, Insert Attendee, add and filter Channelings
SELECT Seances.seance_id, Locations.name, Seances.date
FROM Seances
LEFT JOIN Locations ON Seances.location_id = Locations.location_id;


-- Query for prefill inputs for Update Seance and View Channelings
SELECT seance_id, Locations.name, Seances.date
FROM Seances
LEFT JOIN Locations ON Seances.location_id = Locations.location_id;

-- Colon denotes variable obtained through get request parameters
SELECT seance_id, Locations.name, Seances.date
FROM Seances
LEFT JOIN Locations ON Seances.location_id = Locations.location_id
WHERE Seances.seance_id = :id_input;


-- Query for updating a Seance based on its id
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Seances
SET date = :date_input,
location_id = :location_id_input
WHERE seance_id = :id_input;

-- Query for deleting the Seance with the passed-in id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Seances
WHERE seance_id = :id_input;


-- Query for adding a Method
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Methods (name, description)
VALUES (:name_input, :name_description);

-- Query for getting the full list of methods
SELECT method_id, name, description
FROM Methods;

-- To be used for populating dropdown menu and autofilled textbox for Update Methods and Insert Channeling functionality
SELECT method_id, name
FROM Methods;

-- To be used for edit Methods prefill
-- Colon denotes variable obtained though GET request query parameters
SELECT method_id, name, description
FROM Methods
WHERE method_id = :id_input;

-- Query for updating a method based on id
-- Colon denotes variable that will be obtained through form submission or specific table row
UPDATE Methods
SET name = :name_input,
description = :description_input
WHERE method_id = :id_input;

-- Query for deleting a method based on id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Methods
WHERE method_id = :id_input;

-- Query for adding a Channeling
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO Channelings (medium_id, seance_id, spirit_id, method_id, is_successful, length_in_minutes)
VALUES 
(
:medium_id_from_dropdown_with_medium_names,
:seance_id_from_dropdown_with_seance_locations_and_dates,
:spirit_id_from_dropdown_with_spirit_names,
:method_id_from_dropdown_with_method_names,
:is_successful_input,
:length_in_minutes_input
);

UPDATE Channelings SET
medium_id = :medium_id_from_dropdown_with_medium_names
, spirit_id = :spirit_id_from_dropdown_with_spirit_names
, method_id = :method_id_from_dropdown_with_method_names
, seance_id =  :seance_id_from_dropdown_with_seance_locations_and_dates
, is_successful =  :is_successful_input
, length_in_minutes =  :length_in_minutes_input
WHERE channeling_id =id_input

-- Query for filtering Channelings based on Seance
-- Colon denotes variable that will be obtained through form submission or specific table row
SELECT Channelings.channeling_id, Channelings.medium_id
, Mediums.full_name AS medium_name
, Spirits.spirit_id, Spirits.full_name AS spirit_name
, Channelings.method_id
, Methods.name AS method_name
, Seances.seance_id
, Seances.date, Locations.name AS location_name,
Channelings.is_successful, Channelings.length_in_minutes
FROM Channelings
LEFT JOIN Mediums ON Channelings.medium_id = Mediums.medium_id
LEFT JOIN Spirits ON Channelings.spirit_id = Spirits.spirit_id
LEFT JOIN Methods ON Channelings.method_id = Methods.method_id
LEFT JOIN Seances ON Channelings.seance_id = Seances.seance_id
LEFT JOIN Locations ON Seances.location_id = Locations.location_id
WHERE Seances.seance_id = :seance_id_from_dropdown_with_seance_locations_and_dates;

-- Query for displaying all Channelings with Medium name, Spirit name, Method name, date, and stats
-- Colon denotes variable that will be obtained through form submission or specific table row
SELECT Channelings.channeling_id, Channelings.medium_id
, Mediums.full_name AS medium_name
, Spirits.spirit_id, Spirits.full_name AS spirit_name
, Channelings.method_id
, Methods.name AS method_name
, Seances.seance_id
, Seances.date, Locations.name AS location_name,
Channelings.is_successful, Channelings.length_in_minutes

FROM Channelings
LEFT JOIN Mediums ON Channelings.medium_id = Mediums.medium_id
LEFT JOIN Spirits ON Channelings.spirit_id = Spirits.spirit_id
LEFT JOIN Methods ON Channelings.method_id = Methods.method_id
LEFT JOIN Seances ON Channelings.seance_id = Seances.seance_id
LEFT JOIN Locations ON Seances.location_id = Locations.location_id;

SELECT Channelings.channeling_id, Channelings.medium_id
, Mediums.full_name AS medium_name
, Spirits.spirit_id, Spirits.full_name AS spirit_name
, Channelings.method_id
, Methods.name AS method_name
, Seances.seance_id
, Seances.date, Locations.name AS location_name
 , case when Channelings.is_successful = 0 then 'No'
 when Channelings.is_successful = 1 then 'Yes'
     end is_successful
, Channelings.length_in_minutes
FROM Channelings
LEFT JOIN Mediums ON Channelings.medium_id = Mediums.medium_id
LEFT JOIN Spirits ON Channelings.spirit_id = Spirits.spirit_id
LEFT JOIN Methods ON Channelings.method_id = Methods.method_id
LEFT JOIN Seances ON Channelings.seance_id = Seances.seance_id
LEFT JOIN Locations ON Seances.location_id = Locations.location_id
WHERE Seances.seance_id = id_input;

-- Query for deleting a Channeling based on id
-- Colon denotes variable that will be obtained through form submission or specific table row
DELETE FROM Channelings
WHERE channeling_id = id_input;


-- Query for inserting a record of an Attendee attending a Seance
-- attendee_id obtained through dropdown menu populated with Attendees ids and names
-- seance_id obtained by SeanceAttendee page, which displays the attendees for a specific attendee
-- Colon denotes variable that will be obtained through form submission or specific table row
INSERT INTO SeanceAttendees (attendee_id, seance_id)
VALUES (:attendee_id_input, :seance_id_input);

-- Query for getting a list of names and ids of all Attendees of a Seance
-- seance_id_input is determined by the dropdown menu on the SeanceAttendee page
-- To be used in displaying table on SeanceAttendee page
-- To be used in dropdown for updating SeanceAttendee entry
-- Colon denotes variable that will be obtained through form submission or specific table row

SELECT
SeanceAttendees.seance_id
, Seances.date
, Locations.name
, Attendees.attendee_id
, Attendees.full_name
, SeanceAttendees.seanceattendees_id
FROM SeanceAttendees
LEFT JOIN Attendees ON SeanceAttendees.attendee_id = Attendees.attendee_id
LEFT JOIN Seances ON SeanceAttendees.seance_id = Seances.seance_id
LEFT JOIN Locations ON Seances.location_id = Locations.location_id
WHERE SeanceAttendees.seance_id =  :seance_id_input;

-- same as above but use when filtering records
SELECT
SeanceAttendees.seance_id
, Seances.date
, Locations.name
, Attendees.attendee_id
, Attendees.full_name
, SeanceAttendees.seanceattendees_id
FROM SeanceAttendees
LEFT JOIN Attendees ON SeanceAttendees.attendee_id = Attendees.attendee_id
LEFT JOIN Seances ON SeanceAttendees.seance_id = Seances.seance_id
LEFT JOIN Locations ON Seances.location_id = Locations.location_id
WHERE SeanceAttendees.seance_id =  :seance_id_input;

-- Query for getting the date, location name, and id of all Seances NOT the one currently displayed on the SeanceAttendee page
-- To be used for generating dropdown for Seance Attendee Actually Attended (UPDATE on SeanceAttendees)
-- Colon denotes variable that will be obtained through being on a specific SeanceAttendee page
SELECT Seances.date, Locations.name, Seances.seance_id
FROM Seances
INNER JOIN Locations ON Seances.location_id = Locations.location_id
WHERE seance_id <> :seance_id_from_input;

-- Query for updating an entry in SeanceAttendees to have Attendee attend a different seance than the one listed as attended
-- Colon denotes variable that will be obtained through dropdown or being on a specific SeanceAttendee page
UPDATE SeanceAttendees
SET seance_id = :new_seance_id_input
WHERE attendee_id = :attendee_id_input
AND seance_id = :old_seance_id_input_from_page;

-- Query for deleting a record of a Seance being attended by an Attendee
-- Colon denotes variable that will be obtained through clicking a button on a specific table row
DELETE FROM SeanceAttendees
WHERE seanceattendees_id = :seanceattendee_id_input;
