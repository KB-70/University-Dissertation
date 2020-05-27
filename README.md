# ID: Injection Detector
This project addresses security flaws from SQLi and XSS attacks within an IoT infrastructure, by providing a method of detection for such attacks before they infiltrate a system and become harmful. To tackle this problem, a network application has been developed to detect malicious traffic and prevent its execution on a system before it causes damage.
The mission critical aspects of the system are the server and detection solution, which when reconfigured can be applied within any network.

## Getting Started
All components of the system can be found within the ID: Injection Detector.zip

Minor edits should be made to the server file to adjust the database settings and port numbers as required.

The file db_config3.sql can be launched in MySQL to set up a default database populated with content. This means all data sent to the system can produce data for the client.

### Prerequisites
It is encouraged to have the following present on your local system:
* Python 3.5 (or later)
* MySQL
* Command Line Interface/Terminal

### Installing
The ID: Injection Detector system is packaged for use directly out of the box.


Minor configuration changes need to be made.

The system has been created in it's totality using Python.

A MySQL database user will need to be created. This can be done based on the default settings for the database, or the settings can be changed to suit your needs.

#### Edit the server file
At the top of v4server.py, change the following settings to match your requirements:

```
username = "kb16315"
password = "mqttdbpwd"
database = "mqtt_mock_db"
```

The database setting can remain the same as a database script file is provided which creates this at default, including all its required tables and prepopulates them with revelant initial content. Futher edits can be made to the server to adjust port numbers (if necessary).

#### Install libraries and run program
Key libraries to install:
```
pip install bs4
pip install pymysql
pip install pickle
```

For the system to run properly, the following need to executed in this order:
* MySQL - Start MySQL and log in with the user details defined in v4server.py (If not already running)
* v4server.py - In one terminal window, run the server using the command below
* v4client.py - In another terminal window run the client using the command below

```
python v4server.py
python v4client.py
```

Execution of the client begins the process of automatic generation of data.

You will need to be in the direcotry where the files are stored while in the terminal for any of the files to run.

The system can be stopped from running by termiating the process in either the client or the server.

### Running Tests
Executing the complete system will provide a total overview of the functionality.

Each componect can be executed and tested individually using the raw files and a Python editor (Pycharm is recommended).


## Authors
* K'Ci Beckford - Developer
