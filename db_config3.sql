DROP DATABASE IF EXISTS mqtt_mock_db;
CREATE DATABASE mqtt_mock_db;
USE mqtt_mock_db;

CREATE TABLE Subscribers (
    subscriber_id INT NOT NULL AUTO_INCREMENT,
    subscriber_name VARCHAR(25),
    PRIMARY KEY (subscriber_id)
);

INSERT INTO Subscribers (subscriber_name) VALUES ('Client001');
INSERT INTO Subscribers (subscriber_name) VALUES ('Client002');
INSERT INTO Subscribers (subscriber_name) VALUES ('Client003');
INSERT INTO Subscribers (subscriber_name) VALUES ('Client004');
INSERT INTO Subscribers (subscriber_name) VALUES ('Client005');
INSERT INTO Subscribers (subscriber_name) VALUES ('Client006');
INSERT INTO Subscribers (subscriber_name) VALUES ('Client007');
INSERT INTO Subscribers (subscriber_name) VALUES ('Client008');
INSERT INTO Subscribers (subscriber_name) VALUES ('Client009');
INSERT INTO Subscribers (subscriber_name) VALUES ('Client010');

CREATE TABLE Publishers (
    publisher_id INT NOT NULL AUTO_INCREMENT,
    publisher_name VARCHAR(25),
    PRIMARY KEY (publisher_id)
);

INSERT INTO Publishers (publisher_name) VALUES ('Pub001');
INSERT INTO Publishers (publisher_name) VALUES ('Pub002');
INSERT INTO Publishers (publisher_name) VALUES ('Pub003');
INSERT INTO Publishers (publisher_name) VALUES ('Pub004');
INSERT INTO Publishers (publisher_name) VALUES ('Pub005');
INSERT INTO Publishers (publisher_name) VALUES ('Pub006');
INSERT INTO Publishers (publisher_name) VALUES ('Pub007');
INSERT INTO Publishers (publisher_name) VALUES ('Pub008');
INSERT INTO Publishers (publisher_name) VALUES ('Pub009');
INSERT INTO Publishers (publisher_name) VALUES ('Pub010');

CREATE TABLE Topics (
    topic_id INT NOT NULL AUTO_INCREMENT,
    topic_string VARCHAR(50),
    publisherID INT,
    PRIMARY KEY (topic_id),
    FOREIGN KEY (publisherID) REFERENCES Publishers(publisher_id)
);

INSERT INTO Topics (topic_string, publisherID) VALUES ('house3/livingroom/temp', 1);
INSERT INTO Topics (topic_string, publisherID) VALUES ('house1/proximity', 2);
INSERT INTO Topics (topic_string, publisherID) VALUES ('car1/speed', 3);
INSERT INTO Topics (topic_string, publisherID) VALUES ('car3/proximity', 10);
INSERT INTO Topics (topic_string, publisherID) VALUES ('house2/room1/temp', 9);
INSERT INTO Topics (topic_string, publisherID) VALUES ('car2/speed', 4);
INSERT INTO Topics (topic_string, publisherID) VALUES ('house3/proximity', 7);
INSERT INTO Topics (topic_string, publisherID) VALUES ('house1/bedroom1/temp', 5);
INSERT INTO Topics (topic_string, publisherID) VALUES ('car3/speed', 8);
INSERT INTO Topics (topic_string, publisherID) VALUES ('house1/livingroom/temp', 6);

CREATE TABLE Requests (
    request_id INT NOT NULL AUTO_INCREMENT,
    topicID INT,
    subscriberID INT,
    PRIMARY KEY (request_id),
    FOREIGN KEY (topicID) REFERENCES Topics(topic_id),
    FOREIGN KEY (subscriberID) REFERENCES Subscribers(subscriber_id)
);

INSERT INTO Requests (topicID, subscriberID) VALUES (1, 2);
INSERT INTO Requests (topicID, subscriberID) VALUES (3, 4);
INSERT INTO Requests (topicID, subscriberID) VALUES (2, 5);
INSERT INTO Requests (topicID, subscriberID) VALUES (10, 4);
INSERT INTO Requests (topicID, subscriberID) VALUES (7, 5);
INSERT INTO Requests (topicID, subscriberID) VALUES (6, 8);
INSERT INTO Requests (topicID, subscriberID) VALUES (4, 7);
INSERT INTO Requests (topicID, subscriberID) VALUES (9, 10);
INSERT INTO Requests (topicID, subscriberID) VALUES (5, 1);
INSERT INTO Requests (topicID, subscriberID) VALUES (8, 9);

CREATE TABLE data_points (
    dp_id INT NOT NULL AUTO_INCREMENT,
    dp_value VARCHAR(25),
    value_unit VARCHAR(25),
    post_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    requestID INT,
    PRIMARY KEY (dp_id),
    FOREIGN KEY (requestID) REFERENCES Requests(request_id)
);

INSERT INTO data_points (dp_value, value_unit, requestID) VALUES (25.5, '°C', 1);
INSERT INTO data_points (dp_value, value_unit, requestID) VALUES (100, 'm', 2);
INSERT INTO data_points (dp_value, value_unit, requestID) VALUES (38.2, 'm/s', 3);
INSERT INTO data_points (dp_value, value_unit, requestID) VALUES (18.2, '°C', 4);
INSERT INTO data_points (dp_value, value_unit, requestID) VALUES (45, 'm', 5);
INSERT INTO data_points (dp_value, value_unit, requestID) VALUES (22.8, 'm/s', 6);
INSERT INTO data_points (dp_value, value_unit, requestID) VALUES (4, 'ft', 7);
INSERT INTO data_points (dp_value, value_unit, requestID) VALUES (14, 'm/s', 8);
INSERT INTO data_points (dp_value, value_unit, requestID) VALUES (40.0, '°C', 9);
INSERT INTO data_points (dp_value, value_unit, requestID) VALUES (22.7, '°C', 10);

SELECT * FROM Subscribers;
SELECT * FROM Publishers;
SELECT * FROM Topics;
SELECT * FROM Requests;
SELECT * FROM data_points;
