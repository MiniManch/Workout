import pymysql
import json
import os

# Database connection settings
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'admatainov14',  # Replace with your MySQL root password if set
    'database': 'workout_db',
    'port': 3306  # Optional if using default port 3306
}

dataFile = os.path.join(os.path.dirname(__file__), 'baseData.json')

# SQL queries for creating tables
create_table_queries = {
    'Coach': '''
        CREATE TABLE IF NOT EXISTS Coach (
            CoachID INT PRIMARY KEY AUTO_INCREMENT,
            Name VARCHAR(100),
            Email VARCHAR(100),
            PhoneNumber VARCHAR(20)
        )
    ''',
    'Client': '''
        CREATE TABLE IF NOT EXISTS Client (
            ClientID INT PRIMARY KEY AUTO_INCREMENT,
            Name VARCHAR(100),
            Email VARCHAR(100),
            PhoneNumber VARCHAR(20),
            CoachID INT,
            FOREIGN KEY (CoachID) REFERENCES Coach(CoachID)
        )
    ''',
    'Session': '''
        CREATE TABLE IF NOT EXISTS Session (
            SessionID INT PRIMARY KEY AUTO_INCREMENT,
            Date DATE,
            StartTime TIME,
            Duration INT,
            CoachID INT,
            FOREIGN KEY (CoachID) REFERENCES Coach(CoachID)
        )
    ''',
    'SessionClient': '''
        CREATE TABLE IF NOT EXISTS SessionClient (
            SessionClientID INT PRIMARY KEY AUTO_INCREMENT,
            SessionID INT,
            ClientID INT,
            FOREIGN KEY (SessionID) REFERENCES Session(SessionID),
            FOREIGN KEY (ClientID) REFERENCES Client(ClientID)
        )
    '''
}

# Function to create the database if it doesn't exist
def create_database():
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        port=db_config['port']
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
    cursor.close()
    connection.close()

# Function to create tables
def create_tables(cursor):
    for table_name, create_query in create_table_queries.items():
        cursor.execute(create_query)
        print(f'Table `{table_name}` checked/created.')

# Function to insert data, checking if data already exists
def insert_data(cursor, table, data):
    placeholders = ', '.join(['%s'] * len(data[0]))
    columns = ', '.join(data[0].keys())
    insert_query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
    for entry in data:
        # Check if the data already exists
        select_query = f"SELECT * FROM {table} WHERE {list(entry.keys())[0]} = %s"
        cursor.execute(select_query, (entry[list(entry.keys())[0]],))
        result = cursor.fetchone()
        if result:
            continue
        else:
            cursor.execute(insert_query, tuple(entry.values()))

# Function to setup database
def setup_database():
    # Create the database if it doesn't exist
    create_database()

    # Connect to the newly created database
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # Check and create tables
    create_tables(cursor)
    connection.commit()

    # Load test data from JSON file
    with open(dataFile) as f:
        test_data = json.load(f)

    # Insert test data into tables
    for table, data in test_data.items():
        insert_data(cursor, table.capitalize(), data)
    
    connection.commit()
    cursor.close()
    connection.close()
    print('Test data inserted successfully.')

# Utility function to get a database connection
def get_db_connection():
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        port=db_config['port']
    )
    return connection
