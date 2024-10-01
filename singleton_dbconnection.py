import mysql.connector
from mysql.connector import Error

class MySQLConnectionSingleton:
    _instance = None  # Private class variable to store the single instance of the class

    def __new__(cls, db_config):
        if cls._instance is None:
            try:
                cls._instance = super(MySQLConnectionSingleton, cls).__new__(cls)
                cls._instance.connection = mysql.connector.connect(**db_config)
                print("MySQL connection established")
            except Error as e:
                print(f"Error while connecting to MySQL: {e}")
                cls._instance = None
        return cls._instance

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            MySQLConnectionSingleton._instance = None
            print("MySQL connection closed")


# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',           # Hostname of the MySQL server
    'user': 'root',                # MySQL username
    'password': 'root',            # MySQL password for the user
    'database': 'product_database'  # Name of the database you want to connect to
}

def test_db_connection():
    # Create a singleton instance of MySQLConnectionSingleton
    db_connection = MySQLConnectionSingleton(DB_CONFIG)
    
    # Get the connection
    conn = db_connection.get_connection()

    if conn and conn.is_connected():
        print("Successfully connected to the database.")

        # You can also retrieve some data to confirm the connection
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")  # Get the current database
        db = cursor.fetchone()
        print(f"Connected to database: {db[0]}")

        # Close the cursor
        cursor.close()
    else:
        print("Failed to connect to the database.")

if __name__ == '__main__':
    test_db_connection()
