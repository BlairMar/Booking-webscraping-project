'''url_tester'''

from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import itertools
import boto3
import json
import tempfile

url = 'https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaFCIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4Au2Q-owGwAIB0gIkMjgwYjc1OWMtNWJjNS00MzRmLTkwMzAtYzllNDk0OTc5ZWFh2AIE4AIB&lang=en-us&sid=61c3b046e3496364bf0e0cc43c757203&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaFCIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4Au2Q-owGwAIB0gIkMjgwYjc1OWMtNWJjNS00MzRmLTkwMzAtYzllNDk0OTc5ZWFh2AIE4AIB%3Bsid%3D61c3b046e3496364bf0e0cc43c757203%3Bsb_price_type%3Dtotal%3Bsig%3Dv1w_e9ye7_%26%3B&ss=Barcelona&is_ski_area=0&dest_type=city&checkin_year=2022&checkin_month=1&checkin_monthday=19&checkout_year=2022&checkout_month=1&checkout_monthday=20&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'")
options.add_argument("--lang=en-GB")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get(url)
driver.get_screenshot_as_file("screenshot_-urltester_starturl_UA.png")

dest = ['spain','country']
dates = ['2022','01','01','2022','01','10']
travellers = [1,0,0,0,0,0,0,0,0,0,0,0]
rooms = 1


url2 = f'https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaFCIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4Au2Q-owGwAIB0gIkMjgwYjc1OWMtNWJjNS00MzRmLTkwMzAtYzllNDk0Oc5ZWFh2AIE4AIB&lang=en-us&sid=61c3b046e3496364bf0e0cc43c757203&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaFCIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4Au2Q-owGwAIB0gIkMjgwYjc1OWMtNWJjNS00MzRmLTkwMzAtYzllNDk0OTc5ZWFh2AIE4AIB%3Bsid%3D61c3b046e3496364bf0e0cc43c757203%3Bsb_price_type%3Dtotal%3Bsig%3Dv1w_e9ye7_%26%3B&ss={dest[0]}&is_ski_area=0&dest_type={dest[1]}&checkin_year={dates[0]}&checkin_month={dates[1]}&checkin_monthday={dates[2]}&checkout_year={dates[3]}&checkout_month={dates[4]}&checkout_monthday={dates[5]}&group_adults={travellers[0]}&group_children={travellers[1]}&age={travellers[2]}&age={travellers[3]}&age={travellers[4]}&age={travellers[5]}&age={travellers[6]}&age={travellers[7]}&age={travellers[8]}&age={travellers[9]}&age={travellers[10]}&age={travellers[11]}&no_rooms={rooms}&b_h4u_keep_filters=&from_sf=1'
driver.get(url2)
driver.get_screenshot_as_file("screenshot_urltester_amended_UA.png")

url3 = 'https://www.whatismybrowser.com/detect/what-is-my-user-agent'
driver.get(url3)
driver.get_screenshot_as_file("screenshot_urltester_UA_changeUA.png")