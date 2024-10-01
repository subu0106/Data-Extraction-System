import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import mysql.connector

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


# WebDriver Factory Class
class WebDriverFactory:

    @staticmethod
    def create_driver(driver_type="chrome", headless=True):
        if driver_type.lower() == "chrome":
            options = ChromeOptions()
            options.headless = headless
            driver = webdriver.Chrome(executable_path="c:/WebDrivers/chromedriver.exe", options=options)
        elif driver_type.lower() == "firefox":
            options = FirefoxOptions()
            options.headless = headless
            driver = webdriver.Firefox(executable_path="c:/WebDrivers/geckodriver.exe", options=options)
        else:
            raise ValueError(f"Unknown driver type: {driver_type}")
        
        return driver


# Data Extraction Function
def get_data(driver):
    url = "https://ikman.lk/en/ads/sri-lanka"
    driver.get(url)
    driver.implicitly_wait(10)
    
    data = []
    
    try:
        # Extract product information
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ui-card'))
        )

        for product in products:
            try:
                # Extract product details
                name = product.find_element(By.CSS_SELECTOR, ".ui-card-title").text.strip()
                price = product.find_element(By.CSS_SELECTOR, ".ui-card__price").text.strip()
                location = product.find_element(By.CSS_SELECTOR, ".ui-card-location").text.strip()
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
        print(f"Error loading page: {e}")
    finally:
        driver.quit()

    return data


# Store Data in MySQL using Singleton
def store_in_mysql(data):
    # MySQL configuration
    DB_CONFIG = {
        'user': 'your_username',
        'password': 'your_password',
        'host': 'localhost',
        'database': 'product_scraper'
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

# used if connecting with sql is an issue
# def export_csv(data):
#     df = pd.DataFrame(data)
#     # Save the data to a CSV file
#     df.to_csv("ikman_products.csv", index=False)
#     print(df)  # Print for debugging purposes


# Main Execution
def main():
    # Create a Selenium WebDriver using the Factory
    driver = WebDriverFactory.create_driver(driver_type="chrome", headless=True)
    
    # Scrape data from the website
    data = get_data(driver)
    
    # Store the data in MySQL
    store_in_mysql(data)

    print('DONE')


if __name__ == '__main__':
    main()
