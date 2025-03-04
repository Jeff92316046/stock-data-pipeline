import os
from selenium import webdriver
from selenium.webdriver.common.by import By

XPATH = By.XPATH
TAG_NAME = By.TAG_NAME

options = webdriver.ChromeOptions()
options.add_argument("--headless")
MODE = os.getenv("MODE")

def get_driver(debug=False):
    if debug:
        driver = webdriver.Chrome()
    else:
        if MODE == "prod":
            driver = webdriver.Remote(
                command_executor="http://selenium:4444/wd/hub",
                options=options
            )
        elif MODE == "dev":
            driver = webdriver.Chrome(options=options)
    return driver

driver = get_driver()
