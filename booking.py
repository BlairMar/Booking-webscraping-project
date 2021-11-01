from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager

# from time import sleep
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




# self.driver = webself.driver.Chrome()
url = 'https://www.booking.com'
# self.driver.get(url)

class BeginningStage():

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # self.driver = webdriver.Chrome(options=options)
        options.add_argument("--start-maximized")
        self.hotel_urls = []


    def get_webpage(self):
        url = 'https://www.booking.com'
        webpage = self.driver.get(url)
        time.sleep(3)
        return webpage


    def accept_cookies(self):
        accept = self.driver.find_element_by_id('onetrust-accept-btn-handler')
        accept.click()


    # def choose_option_1(self):
    #     search_bar = self.driver.find_element_by_id('ss')
    #     search_bar.click()
    #     first_option = self.driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[1]/div[1]/div[1]/ul[1]/li[2]')
    #     first_option.click()

    def select_search_bar(self, destination):
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
        search_bar = self.driver.find_element_by_id('ss')
        search_bar.clear()
        search_bar.send_keys(destination)
        first_result = WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'li[data-i="0"]')))
        first_result.click()

    def choose_dates(self):
        check_in = self.driver.find_element_by_css_selector('td[data-date="2021-11-22"]')
        check_out = self.driver.find_element_by_css_selector('td[data-date="2021-11-23"]')
        check_in.click()
        check_out.click()


    def click_search_button(self):
        search_button = self.driver.find_element_by_css_selector('button[type="submit"]')
        search_button.click()

    def get_hotel_urls(self):
        hotel_container = self.driver.find_element_by_id('search_results_table')
        hotel_list = hotel_container.find_elements_by_css_selector('div[data-testid="property-card"]')
        #WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_all_elements_located(
                    #(By.CSS_SELECTOR, 'div[data-testid="property-card"]')))
        

        for element in hotel_list:
            hotel_url = element.find_element_by_xpath('.//a').get_attribute('href')
            self.hotel_urls.append(hotel_url)
        # print(self.hotel_urls)

    # def create_csv(self):
    #     open('hotels.csv' Header=['Name','Price']

    def get_hotel_details(self):
        hotel_detail_dict_list = []
        # url_counter = 0
            # url_counter += 1
        for idx in range(0, len(self.hotel_urls)):
            hotel_detail_dict = {'Name' : None, 'Room_Type': None ,'Price' : None, 'Address': None, 'Deals': 'None', 
                            'Wifi': 0}
            # hotel_detail_dict = {'Name' : None, 'Room_Type': None ,'Price' : None, 'Address': None, 'Deals': 'None', 
            #             'Wifi': 0, 'Restaurant': 0, 'Room_Service': 0, 'Private_Parking': 0, 'Disabled_Facilities': 0,
            #             '24hr_FrontDesk': 0}
            self.driver.get(self.hotel_urls[idx])

            hotel_name = self.driver.find_element_by_id("hp_hotel_name")
            hotel_detail_dict['Name'] = hotel_name.text
            # hotel_detail_dict['Name'].append(hotel_name.text)

            hotel_room_type = self.driver.find_element_by_css_selector('span[class="hprt-roomtype-icon-link "]')
            hotel_detail_dict['Room_Type'] = hotel_room_type.text
            # hotel_detail_dict['Room_Type'].append(hotel_room_type.text)

            hotel_price = self.driver.find_element_by_class_name('prco-valign-middle-helper')
            hotel_detail_dict['Price'] = hotel_price.text
            # hotel_detail_dict['Price'].append(hotel_price.text)

            hotel_address = self.driver.find_element_by_css_selector('span[data-node_tt_id="location_score_tooltip"]')
            hotel_detail_dict['Address'] = hotel_address.text    
            # hotel_detail_dict['Address'].append(hotel_address.text)



            # try:
            # hotel_deal_temp = self.driver.find_element_by_css_selector('span[class="bui-badge__text"]').text
            # hotel_detail_dict['Deals'] = hotel_deal_temp
            # hotel_detail_dict['Deals'].append(hotel_deal_temp)
            # hotel_wifi_temp = self.driver.find_element_by_css_selector('div[data-name-en="WiFi everywhere"]')
            # hotel_restaurant_temp = self.driver.find_element_by_css_selector('div[data-name-en="Restaurant"]')
            # hotel_room_service_temp = self.driver.find_element_by_css_selector('div[data-name-en="Room-service"]')
            # hotel_private_parking_temp = self.driver.find_element_by_css_selector('div[data-name-en="Private parking"]')
            # hotel_disabled_facilities_temp = self.driver.find_element_by_css_selector('div[data-name-en="Rooms/Facilities for Disabled"]')
            # hotel_24hr_desk_temp = self.driver.find_element_by_css_selector('div[data-name-en="24 hour Front Desk"]')
            # if hotel_wifi_temp:
            #     hotel_detail_dict['Wifi'] = 1
            # if hotel_restaurant_temp:
            #     hotel_detail_dict['Restaurant'] = 1
            # if hotel_room_service_temp:
            #     hotel_detail_dict['Room-service'] = 1
            # if hotel_private_parking_temp:
            #     hotel_detail_dict['Private_Parking'] = 1
            # if hotel_disabled_facilities_temp:
            #     hotel_detail_dict['Disabled_Facilities'] = 1
            # if hotel_24hr_desk_temp:
            #     hotel_detail_dict['24hr_FrontDesk'] = 1


            # except NoSuchElementException:
            #     pass

            hotel_detail_dict_list.append(hotel_detail_dict)
            
        print(hotel_detail_dict_list)
        df = pd.json_normalize(hotel_detail_dict_list) 
        df.to_csv('hotels.csv') 


    

    def click_next_page(self):
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
        page_count = 0
        # pages_remaining = self.driver.find_element_by_xpath('//*[@id="search_results_table"]/div[1]/div/div/div/div[6]/div[2]/nav/div/div[2]/ol/li[6]').get_attribute('innerText')
        # print(pages_remaining)
        # # print(type(pages_remaining))
        # number_pages = int(pages_remaining)
        pages_remaining = True

        # print(type(number_pages))
        # for _ in range(number_pages):
        # while pages_remaining: - bring back when launching, comment out/remove line for_ in range(2) and next line

            # try:
            #     self.driver.execute_script("window.history.go(-1)")
            # except NoSuchElementException:
            #     time.sleep(0.3)
            #     continue

        for _ in range(2):
            if page_count < 2:
                try:
                    self.get_hotel_urls()
                    # next_page = self.driver.find_element_by_xpath('//*[@id="search_results_table"]/div[6]/nav/ul/li[3]/a')
                    # next_page = WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located(
                    # (By.XPATH, '//*[@id="search_results_table"]/div[6]/nav/ul/li[3]/a')))
                    # next_page.click()
                    # next_page = WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located(
                    # (By.CSS_SELECTOR, 'button[aria-label="Next page"]')))
                    next_page = WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div[class="ce83a38554 _ea2496c5b"]')))
                    next_page.click()
                    print('this works')
                    self.driver.refresh()
                    page_count += 1
                    print(page_count)
                
                except:
                    pass
                    # pages_remaining = False
            
        self.get_hotel_details()    

        

first_booking = BeginningStage()
first_booking.get_webpage()
first_booking.accept_cookies()

# first_booking.choose_option_1()
first_booking.select_search_bar('Algeria')

first_booking.choose_dates()
first_booking.click_search_button()
# first_booking.duplicate_tab()
# first_booking.apply_star_rating(2)
# first_booking.budget_filters(25)
first_booking.get_hotel_urls()
first_booking.click_next_page()
# first_booking.get_hotel_details()
# first_booking.write_to_csv()