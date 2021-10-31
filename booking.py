from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

# from time import sleep
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import pandas as pd




# self.driver = webself.driver.Chrome()
url = 'https://www.booking.com'
# self.driver.get(url)

class BeginningStage():

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        # self.driver = webdriver.Chrome(options=options)
        options.add_argument("--start-maximized")


    def get_webpage(self):
        url = 'https://www.booking.com'
        webpage = self.driver.get(url)
        time.sleep(3)
        return webpage


    def accept_cookies(self):
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
        check_out = self.driver.find_element_by_css_selector('td[data-date="2021-11-23"]')
        check_out.click()

    def click_search_button(self):
        search_button = self.driver.find_element_by_css_selector('button[type="submit"]')
        search_button.click()

    def get_hotel_urls(self):
        hotel_container = self.driver.find_element_by_id('search_results_table')
        hotel_list = hotel_container.find_elements_by_css_selector('div[data-testid="property-card"]')
        self.hotel_urls = []

        for element in hotel_list:
            hotel_url = element.find_element_by_xpath('.//a').get_attribute('href')
            self.hotel_urls.append(hotel_url)
        # print(self.hotel_urls)

    # def create_csv(self):
    #     open('hotels.csv' Header=['Name','Price']

    def get_hotel_details(self):
        hotel_detail_dict_list = []
        url_counter = 0
        for url in self.hotel_urls:
            url_counter += 1
            hotel_detail_dict = {'Name' : None, 'Price' : None }
            self.driver.get(url)

            hotel_name = self.driver.find_element_by_id("hp_hotel_name")
            hotel_detail_dict['Name'] = hotel_name.text

            hotel_price = self.driver.find_element_by_class_name('prco-valign-middle-helper')

            hotel_detail_dict['Price'] = hotel_price.text

            hotel_detail_dict_list.append(hotel_detail_dict)

        #print(hotel_detail_dict_list)
        df = pd.json_normalize(hotel_detail_dict_list)
        df.to_csv('hotels.csv') 
        #^-- don't know best way to get this to work for multiple pages\ 
        # we would want it to print to the csv through each call of this\
        # function to make sure it is appending the information each time\
        # (on each new page, the dict and df would be wiped/start from scratch?)
        # have tried df.to_csv('hotels.csv', mode = a, Header = None) to append but may get same issue.


    def click_next_page(self):
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
        pages_remaining = True
        while pages_remaining:
            self.get_hotel_urls()
            self.get_hotel_details()

            try:
                next_page = WebDriverWait(self.driver, 10, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="search_results_table"]/div[6]/nav/ul/li[3]/a')))
                next_page.click()
                self.driver.refresh()
                print('this works')

            except TimeoutException:
                pages_remaining = False
                print('this does not work')



first_booking = BeginningStage()
first_booking.get_webpage()
first_booking.accept_cookies()
first_booking.click_search_bar()
first_booking.choose_option_1()
first_booking.check_in_date()
first_booking.check_out_date()
first_booking.click_search_button()
# first_booking.apply_star_rating(2)
# first_booking.budget_filters(25)
first_booking.get_hotel_urls()
first_booking.get_hotel_details()
#first_booking.click_next_page()
# first_booking.write_to_csv()