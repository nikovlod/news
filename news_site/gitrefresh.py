from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time


def gitrefresh():
    print("Refreshing git repo...")
# Set up Firefox options
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run in headless mode


# Set the path to the Geckodriver executable
    geckodriver_service = Service('/usr/local/bin/geckodriver')

# Initialize the WebDriver
    driver = webdriver.Firefox(service=geckodriver_service, options = firefox_options)

    


# Example usage: open a webpage
    driver.get('https://github.com/nikovlod/news')

    time.sleep(10)

    page_source = driver.page_source





#print(content.text)

# Quit the WebDriver
    driver.quit()

