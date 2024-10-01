# Web Scraping with Selenium and Storing in MySQL

[![Selenium](https://img.shields.io/badge/Selenium-Web%20Scraping-green)](https://www.selenium.dev/)  
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)  
[![MySQL](https://img.shields.io/badge/MySQL-Database-orange.svg)](https://www.mysql.com/)



## Project Overview

This project demonstrates web scraping using **Selenium** to extract product information from [Ikman.lk](https://ikman.lk). The extracted data, including product name, price, location, and phone number, is then stored in a **MySQL database**. The project is designed using two software design patterns—**Singleton** for database connections and **Factory** for creating Selenium WebDriver instances.

By following this project, you will learn how to:
- Set up Selenium for Python.
- Scrape dynamic web pages using Selenium.
- Use the Singleton pattern to manage a single database connection instance.
- Use the Factory pattern to create WebDriver instances dynamically.
- Store scraped data

## Setting up Selenium
To begin web scraping with Selenium, you'll need to install the Selenium package and set up the appropriate WebDriver for your browser.

### Installing Selenium
To install Selenium, simply run:
 "pip install selenium"

### Selenium Drivers
To use Selenium, you need a browser driver. In this example, we use Google Chrome. Ensure you have Chrome installed, then download the corresponding ChromeDriver for your browser version from here.

Once downloaded, place the chromedriver.exe file in a folder (e.g., C:/WebDrivers/), and note the path for use in your Python script.

# Web Scraping Project

## Data Extraction

This script is designed to scrape product data from a dynamic website. The following product details are extracted:

- **Name**: The name of the product.
- **Price**: The price of the product.
- **Location**: The location of the product listing.
- **Phone Number**: The phone numbers of the owner.

## Storing Data in MySQL

After scraping, the extracted data is stored in a MySQL database. This is achieved using the `MySQLConnectionSingleton` class, which ensures that only one connection to the database is active at any given time. This approach enhances performance and resource management.

## Design Patterns Used

### Singleton Pattern for Database Connection

We implement the Singleton Pattern to ensure that only one instance of the database connection is created and shared across the application. This prevents multiple unnecessary connections and optimizes resource usage.

```python
class MySQLConnectionSingleton:
    # Singleton pattern implementation

