from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions

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
