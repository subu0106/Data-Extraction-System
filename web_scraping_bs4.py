import pandas as pd
import mysql.connector
import requests
from bs4 import BeautifulSoup

# Singleton Database Connection
class MySQLConnectionSingleton:
    _instance = None

    def __new__(cls, db_config):
        if cls._instance is None:
            try:
                cls._instance = super(MySQLConnectionSingleton, cls).__new__(cls)
                cls._instance.connection = mysql.connector.connect(**db_config)
                print("MySQL connection established")
            except mysql.connector.Error as e:
                print(f"Error while connecting to MySQL: {e}")
                cls._instance = None
        return cls._instance

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            MySQLConnectionSingleton._instance = None
            print("MySQL connection closed")


# Data Extraction Function using Beautiful Soup
def get_data(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return []

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []

    try:
        # Extract product information
        products = soup.select('.ui-card')  # Adjust the selector based on the actual structure

        for product in products:
            try:
                # Extract product details
                name = product.select_one(".ui-card-title").text.strip()
                price = product.select_one(".ui-card__price").text.strip()
                location = product.select_one(".ui-card-location").text.strip()
                phone_number = "No Phone Number"  # Placeholder for phone numbers

                data.append({
                    'name': name,
                    'price': price,
                    'location': location,
                    'phone_number': phone_number
                })

            except Exception as e:
                print(f"Error extracting product details: {e}")

    except Exception as e:
        print(f"Error parsing page: {e}")

    return data


# Store Data in MySQL using Singleton
def store_in_mysql(data):
    # MySQL configuration
    DB_CONFIG = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'product_database'
    }

    # Get Singleton instance of the database connection
    db_instance = MySQLConnectionSingleton(DB_CONFIG)
    connection = db_instance.get_connection()

    try:
        cursor = connection.cursor()

        for record in data:
            cursor.execute("""
                INSERT INTO ikman_products (name, price, location, phone_number)
                VALUES (%s, %s, %s, %s)
            """, (record['name'], record['price'], record['location'], record['phone_number']))

        connection.commit()
        print(f"{cursor.rowcount} records inserted into the database.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            db_instance.close_connection()


# Main Execution
def main():
    url = "https://ikman.lk/en/ads/sri-lanka"
    
    # Scrape data from the website
    data = get_data(url)
    
    # Store the data in MySQL
    store_in_mysql(data)

    print('DONE')


if __name__ == '__main__':
    main()
