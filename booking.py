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
        hotel_list = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="property-card"]')))
        hotel_list = hotel_container.find_elements_by_css_selector('div[data-testid="property-card"]')

        for element in hotel_list:
            hotel_url = element.find_element_by_xpath('.//a').get_attribute('href')
            self.hotel_urls.append(hotel_url)
        print(self.hotel_urls)

    # def create_csv(self):
    #     open('hotels.csv' Header=['Name','Price']

    def get_hotel_details(self):
        hotel_detail_dict_list = []
        # url_counter = 0
            # url_counter += 1
        for url in self.hotel_urls:
            hotel_detail_dict = {'Name' : None, 'Room_Type': None ,'Price' : None, 'Address': None, 'Deals': 'None', 
                            'Wifi': 0}
            # hotel_detail_dict = {'Name' : None, 'Room_Type': None ,'Price' : None, 'Address': None, 'Deals': 'None', 
            #             'Wifi': 0, 'Restaurant': 0, 'Room_Service': 0, 'Private_Parking': 0, 'Disabled_Facilities': 0,
            #             '24hr_FrontDesk': 0}
            self.driver.get(url)
            hotel_name = self.driver.find_element_by_id("hp_hotel_name")
            hotel_detail_dict['Name'] = hotel_name.text

            hotel_room_type = self.driver.find_element_by_css_selector('span[class="hprt-roomtype-icon-link "]')
            hotel_detail_dict['Room_Type'] = hotel_room_type.text

            hotel_price = self.driver.find_element_by_class_name('prco-valign-middle-helper')
            hotel_detail_dict['Price'] = hotel_price.text

            hotel_address = self.driver.find_element_by_css_selector('span[data-node_tt_id="location_score_tooltip"]')
            hotel_detail_dict['Address'] = hotel_address.text    
 

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
        self.driver.quit()


    

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
                   # next_page = self.driver.find_element_by_xpath('//*[@id="search_results_table"]/div[6]/nav/ul/li[3]/a')
                    # next_page = WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located(
                    # (By.XPATH, '//*[@id="search_results_table"]/div[6]/nav/ul/li[3]/a')))
                    # next_page.click()
                    # next_page = WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located(
                    # (By.CSS_SELECTOR, 'button[aria-label="Next page"]')))
                    next_page = WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div[class="ce83a38554 _ea2496c5b"]')))
                    next_page.click()
                    self.get_hotel_urls()
                    print('this works')
                    self.driver.refresh()
                    page_count += 1
                    print(page_count)
                    
                
                except:
                    pass
                    # pages_remaining = False
            
        self.get_hotel_details()    

    def adults(self,adult_count):
            #adults=self.driver.find_elements_by_xpath(class='bui-u-sr-only')
            container=self.driver.find_element_by_xpath('//*[@id="xp__guests__toggle"]/span[2]')
            container.click()
            if adult_count > 2:
                while adult_count !=2:
                    add_adult=self.driver.find_element_by_xpath('//*[@id="xp__guests__inputs-container"]/div/div/div[1]/div/div[2]/button[2]')
                    add_adult.click()
                    adult_count -= 1
            elif adult_count == 1:
                add_adult=self.driver.find_element_by_xpath('//*[@id="xp__guests__inputs-container"]/div/div/div[1]/div/div[2]/button[1]')
                add_adult.click()

    def children(self,children_count=0,age1=0,age2=0,age3=0,age4=0,age5=0,age6=0,age7=0,age8=0,age9=0,age10=0):
        if children_count>0:
            child_ages=[age2+2,age3+2,age4+2,age5+2,age6+2,age7+2,age8+2,age9+2,age10+2]
            children=self.driver.find_element_by_xpath('//*[@id="xp__guests__inputs-container"]/div/div/div[2]/div/div[2]/button[2]')
            children.click()
            choose_age=self.driver.find_element_by_xpath(f'//*[@id="xp__guests__inputs-container"]/div/div/div[3]/select/option[{age1+2}]')
            choose_age.click()

        if children_count>1:
            count =1
            for child in range(1,children_count):
                age=child_ages[count-1]
                count+=1
                print(age)
                children=self.driver.find_element_by_xpath('//*[@id="xp__guests__inputs-container"]/div/div/div[2]/div/div[2]/button[2]')
                children.click()
                choose_age=self.driver.find_element_by_xpath(f'//*[@id="xp__guests__inputs-container"]/div/div/div[3]/select[{count}]/option[{age}]')
                choose_age.click()

    
    def rooms(self,number_of_rooms=1):
        if number_of_rooms > 1:
            while number_of_rooms !=1:
                add_room=self.driver.find_element_by_xpath('//*[@id="xp__guests__inputs-container"]/div/div/div[4]/div/div[2]/button[2]/span')
                add_room.click()
                number_of_rooms -= 1        

first_booking = BeginningStage()
first_booking.get_webpage()
first_booking.accept_cookies()

# first_booking.choose_option_1()
first_booking.select_search_bar('Algeria')


first_booking.choose_dates()
first_booking.adults(2)
first_booking.children(2,4,14)
first_booking.rooms(2)
first_booking.click_search_button()
# first_booking.duplicate_tab()
# first_booking.apply_star_rating(2)
# first_booking.budget_filters(25)
first_booking.get_hotel_urls()
first_booking.click_next_page()
#first_booking.get_hotel_details()
# first_booking.write_to_csv()