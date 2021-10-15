from selenium import webdriver
import time
# from time import sleep
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebdriverWait
from selenium.webdriver.support import expected_conditions as EC

# self.driver = webself.driver.Chrome()
url = 'https://www.booking.com'
# self.driver.get(url)

class BeginningStage():

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)
        # self.self.driver_path = self.driver_path
        # self.implicitly_wait(10)
        # self.results = []

    def get_webpage(self):
        url = 'https://www.booking.com'
        webpage = self.driver.get(url)
        time.sleep(3)
        return webpage


    def accept_cookies(self):
        # url = 'https://www.booking.com'
        # self.driver.get(url)
        accept = self.driver.find_element_by_id('onetrust-accept-btn-handler')
        accept.click()

    def click_search_bar(self):
        search_bar = self.driver.find_element_by_id('ss')
        search_bar.click()

    def choose_option_1(self):
        first_option = self.driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[1]/div[1]/div[1]/ul[1]/li[2]')
        first_option.click()

    def check_in_date(self):
        check_in = self.driver.find_element_by_css_selector('td[data-date="2021-11-22"]')
        check_in.click()

    def check_out_date(self):
        check_out = self.driver.find_element_by_css_selector('td[data-date="2021-11-29"]')
        check_out.click()

    def click_search_button(self):
        search_button = self.driver.find_element_by_css_selector('button[type="submit"]')
        search_button.click()

    def get_hotel_card(self):
        results = {"Hotel Name" : [],"Hotel Price":[],"Hotel Distance":[]}
        property_card = self.driver.find_elements_by_class_name('sr_property_block')
        for items in property_card:
            hotel_name = items.find_element_by_class_name('sr-hotel__name').get_attribute('innerHTML').strip()
            hotel_price = items.find_element_by_class_name('prco-valign-middle-helper').get_attribute('innerHTML').strip()
            hotel_distance = items.find_element_by_class_name('sr_card_address_line__user_destination_address').get_attribute('innerHTML').strip()
            # hotel_description = items.find_element_by_class_name('_5e1912b06f')
            # print(f'hotel description - {hotel_description}')
            # hotel_rating = items.find_element_by_class_name('eb2161f400 e5a32fd86b').get_attribute('innerHTML').strip()
            # print(f'hotel rating - {hotel_rating}')
            # hotel_address = items.find_element_by_css_selector('span[data-testid="address"]')
            # print(f'hotel address - {hotel_address}')
            results['Hotel Name'].append(hotel_name)
            results['Hotel Price'].append(hotel_price)
            results['Hotel Distance'].append(hotel_distance)     
        print(results)
        return results

first_booking = BeginningStage()
first_booking.get_webpage()
first_booking.accept_cookies()
first_booking.click_search_bar()
first_booking.choose_option_1()
first_booking.check_in_date()
first_booking.check_out_date()
first_booking.click_search_button()
first_booking.get_hotel_card()
