from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class SeleniumContext:
    def __init__( self, url):
        self.url = url

    def __enter__(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        return self.driver

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.driver.quit()

def autoscroll_extraction( url, *, target_class, end_of_page_class, single_object_transform):
    with SeleniumContext( url) as webpage:
        while True:
            objects = webpage.find_elements_by_class_name(target_class)
            try:
                webpage.find_element_by_class_name( end_of_page_class)
                return [ eval( single_object_transform) for object in objects]
            except:
                webpage.execute_script("return arguments[0].scrollIntoView();", objects[-1])
                time.sleep(0.1)

def safe_soup( target_url):
    import requests
    from bs4 import BeautifulSoup

    response = requests.get( target_url)
    if response.status_code == requests.codes.ok:
        return BeautifulSoup( response.text, 'html.parser')
