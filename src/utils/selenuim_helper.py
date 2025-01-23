from selenium import webdriver
from contextlib import contextmanager
from selenium.webdriver.common.by import By

XPATH = By.XPATH
options = webdriver.ChromeOptions()
options.add_argument("--headless")


@contextmanager
def get_driver(debug=False):
    if debug:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Chrome(options=options)
    try:
        yield driver
    finally:
        driver.close()
