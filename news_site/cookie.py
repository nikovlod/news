from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import json


def get_cookie():
# Set up Firefox options
    firefox_options = Options()
    #firefox_options.add_argument("--headless")  # Run in headless mode
    #firefox_options.set_preference("javascript.enabled", False)


# Set the path to the Geckodriver executable
    geckodriver_service = Service('/usr/local/bin/geckodriver')

# Initialize the WebDriver
    driver = webdriver.Firefox(service=geckodriver_service, options = firefox_options)

# Navigate to the website
    driver.get('https://archive.ph/CGHFR')

# Perform any necessary login or actions to get the cookies

# Get cookies
    cookies = driver.get_cookies()

# Save cookies to a file
    with open('cookies.json', 'w') as file:
        json.dump(cookies, file)
    
    driver.quit()

if __name__ == "__main__":
    get_cookie()

