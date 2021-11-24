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


# self.driver = webself.driver.Chrome()
url = 'https://www.booking.com'
# self.driver.get(url)

class BeginningStage():
    ''' This class is used to scrape data from Booking.com
    '''

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # self.driver = webdriver.Chrome(options=options)
        self.hotel_urls = []
        self.dates=[] # Checkin and checkout dates to be saved as checkinyyyy, checkinmm, checkindd, checkoutyyyy, checkoutmm & checkoutdd
        self.destination=[]# Destiantion is saved in the list, however curretnly set to search only one destination
        self.page_counter = 0
        self.s3_client = boto3.client('s3')


    def get_webpage(self):
        '''This function is used to fetch a webpage using ChromeDriver.
        
        Returns:
            webpage'''
        url = 'https://www.booking.com'
        webpage = self.driver.get(url)
        time.sleep(3)
        return webpage


    def accept_cookies(self):
        '''This function is used to click the 'accept cookies' button that appears on the webpage'''
        accept = self.driver.find_element(By.ID,'onetrust-accept-btn-handler')
        accept.click()

    def choose_option_1(self):
        '''This function is used to click the first option that appears when the Booking.com search bar is clicked'''
        search_bar = self.driver.find_element(By.ID,'ss')
        search_bar.click()
        first_option = self.driver.find_element(By.XPATH,'//*[@id="frm"]/div[1]/div[1]/div[1]/div[1]/ul[1]/li[2]')
        first_option.click()

    def choose_dates(self):
        '''This function is used to choose dates (auto set to 22nd and 23rd December)'''
        # TODO: set this so dates can be chosen by user
        check_in = self.driver.find_element(By.CSS_SELECTOR,'td[data-date="2021-12-22"]')
        check_out = self.driver.find_element(By.CSS_SELECTOR,'td[data-date="2021-12-23"]')
        check_in.click()
        check_out.click()



    def click_search_button(self):
        '''This function clicks the search button'''
        search_button = self.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]')
        search_button.click()
        curl = self.driver.current_url
        print(curl)
        self.get_dates()
        self.get_dates()
        print(self.dates)
        ck_yr = curl.index("checkin_year=")
        ck_mn = curl.index("checkin_month=")
        ck_dy = curl.index("checkin_monthday=")
        co_yr = curl.index("checkout_year=")
        co_mn = curl.index("checkout_month=")
        co_dy = curl.index("checkout_monthday=")
        
        curl = curl[:ck_yr+13] + self.dates[0]  + curl[ck_yr+17:ck_mn+14] + self.dates[1] + curl[ck_mn+16:ck_dy+17] + self.dates[2] + curl[ck_dy+19:co_yr+14] + self.dates[3] + curl[co_yr+18:co_mn+15] + self.dates[4] + curl[co_mn+17:co_dy+18] + self.dates[5] +curl[co_dy+20:]
        
        webpage = self.driver.get(curl)
        #time.sleep(3)
        search_button = self.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]')
        search_button.click()
        return webpage
    
    def get_dates(self):
        travel_dt = input('Enter Travel date (yyyy-mm-dd): ')
        self.dates.append(travel_dt[0:4])
        self.dates.append(travel_dt[5:7])
        self.dates.append(travel_dt[8:10])
        
        

    def get_hotel_urls(self):
        '''This function is used to retrieve a list of hotel URLs from the search result container.
        
        Returns:
            list: list of hotel URLs'''
        time.sleep(5)
        # should work instead of needing sleep each round, but for some reason doesn't - sometimes elements are stale again?
        # try:
        #     WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div/div[3]/div[1]/div[1]/div[3]/div[4]/div[1]/div/div/div/div[5]/div[27]/div[1]/div[2]/div/div[4]/div/div[1]/div/div/div/div[3]/div[1]')))
        #     WebDriverWait(self.driver,10).until_not(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div/div[3]/div[1]/div[1]/div[3]/div[4]/div[1]/div/div/div/div[5]/div[27]/div[1]/div[2]/div/div[4]/div/div[1]/div/div/div/div[3]/div[1]')))

        # except TimeoutException:
        #     pass

        # finally:
        hotel_container = self.driver.find_element(By.ID,'search_results_table')
        hotel_list = hotel_container.find_elements(By.CSS_SELECTOR,'div[data-testid="property-card"]')

        for element in hotel_list:
            hotel_url = element.find_element(By.XPATH,'.//a')
            hotel_url = hotel_url.get_attribute('href')
            self.hotel_urls.append(hotel_url)
        self.page_counter += 1
        print(f'Pages visited: {self.page_counter}')
        print(len(self.hotel_urls))

        # for checking errors:
        # for i,element in enumerate(hotel_list):
            
        #     print(i)
        #     print(element)
        #     hotel_url = element.find_element_by_xpath('.//a')
        #     print(hotel_url.text)
        #     hotel_url = hotel_url.get_attribute('href')
        #     print(hotel_url)
        #     print()
        #     self.hotel_urls.append(hotel_url)
        # #print(self.hotel_urls)
        # self.page_counter += 1
        # print(f'Pages visited: {self.page_counter}')
        # print(len(self.hotel_urls))


    def get_hotel_details(self):
        '''This function is used to retrieve individual hotel details.

            Returns:
                list: list of dictionaries containing individual hotel details '''
        print('gathering hotel data')
        hotel_detail_dict_list = []
        # url_counter = 0
            # url_counter += 1
        for i, url in enumerate(self.hotel_urls):
            print(i+1)
            hotel_detail_dict = {'Name' : None, 'Room_Type': None ,'Price' : None, 'Address': None, 'Deals': None, 
                            'Wifi' : 0,'Rating' : None,'Facilities' : None, 'Star': None}
            # hotel_detail_dict = {'Name' : None, 'Room_Type': None ,'Price' : None, 'Address': None, 'Deals': 'None', 
            #             'Wifi': 0, 'Restaurant': 0, 'Room_Service': 0, 'Private_Parking': 0, 'Disabled_Facilities': 0,
            #             '24hr_FrontDesk': 0}
            self.driver.get(url)
            try:
                hotel_name = self.driver.find_element(By.ID,"hp_hotel_name")
                hotel_detail_dict['Name'] = hotel_name.text
            except:
                 hotel_detail_dict['Name'] = 'Name Not Found'           
            try:
                hotel_room_type = self.driver.find_element(By.CSS_SELECTOR,'span[class="hprt-roomtype-icon-link "]')
                hotel_detail_dict['Room_Type'] = hotel_room_type.text
            except:
                hotel_detail_dict['Room_Type'] = 'Room Type Not Found'

            try:
                hotel_price = self.driver.find_element(By.CLASS_NAME,'prco-valign-middle-helper')
                hotel_detail_dict['Price'] = hotel_price.text
            except:
                hotel_detail_dict['Price'] = 'Price Not Found'
            try:    
                hotel_address = self.driver.find_element(By.CSS_SELECTOR,'span[data-node_tt_id="location_score_tooltip"]')
                hotel_detail_dict['Address'] = hotel_address.text  
            except:
                hotel_detail_dict['Address'] = 'Address Not Found'   
            try:    
                hotel_rating = self.driver.find_element(By.XPATH,'//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div/div[1]')
                hotel_detail_dict['Rating'] = hotel_rating.text  
            except:
                hotel_detail_dict['Rating'] = 'Rating Not Found'   
            try:    
                hotel_facilities = self.driver.find_element(By.XPATH,'//*[@id="basiclayout"]/div[1]/div/div[2]/div[16]')
                temp_list=hotel_facilities.text
                temp_list=temp_list[24:] # used to remove the phrase 'Most popular facilities'
                hotel_detail_dict['Facilities'] = temp_list
            except:
                hotel_detail_dict['Facilities'] = 'No Facilities Found'   
            print(hotel_detail_dict)
            
            # For some reason I am unable to get the stars part working.
            try:    
                hotel_stars  = self.driver.find_element(By.XPATH,'//*[@id="wrap-hotelpage-top"]/div[1]/span/span[1]/div/div/span/div/span')
                hotel_detail_dict['Star'] = hotel_stars.text  
                print(hotel_stars.text)
            except:
                hotel_detail_dict['Star'] = 'Stars unavailable'   
                        
            
            
            hotel_detail_dict_list.append(hotel_detail_dict)
            with tempfile.TemporaryDirectory() as temp_dir:
                with open(f'{temp_dir}/hotel_dict{i+1}.json','w') as file:
                    json.dump(hotel_detail_dict,file)
                    self.s3_client.upload_file(f'{temp_dir}/hotel_dict{i+1}.json', 'bookingbucket', f'hotel_jsons/hotel{i+1}.json')
            
        print('gathered all hotel data')
        df = pd.json_normalize(hotel_detail_dict_list) 
        df.to_csv('hotels.csv')
        self.driver.quit()
        self.s3_client.upload_file('hotels.csv', 'bookingbucket', 'hotels.csv')
    

    def click_next_page(self):
        '''This function is used to click the next page of search results'''
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
        pages_remaining = True
        page_count = 0

        # # ##USE TO SCRAPE ALL PAGES
        # while pages_remaining:
        #     try:
        #         time.sleep(3)
        #         next_page = WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="ce83a38554 _ea2496c5b"]')))
        #         next_page.click()
        #         self.get_hotel_urls()
        #         self.driver.refresh()
        #     except:
        #         pages_remaining = False

        #USE TO TEST SMALL RANGE OF PAGES
        for page in range(0):
            if page_count < 1:
                #try:
                    time.sleep(3)
                    next_page = WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="ce83a38554 _ea2496c5b"]')))
                    next_page.click()
                    self.get_hotel_urls()
                    self.driver.refresh()
                    page_count += 1
                # #except:
                #     pass
        self.get_hotel_details()    

    def adults(self,adult_count):
        '''This function is used to define the number of adults to be included in the search
            
            Attributes:
                adult_count: int, the number of adults to include in the search'''
            
        container=self.driver.find_element(By.XPATH,'//*[@id="xp__guests__toggle"]/span[2]')
        container.click()
        if adult_count > 2:
            while adult_count !=2:
                add_adult=self.driver.find_element(By.XPATH,'//*[@id="xp__guests__inputs-container"]/div/div/div[1]/div/div[2]/button[2]')
                add_adult.click()
                adult_count -= 1
        elif adult_count == 1:
            add_adult=self.driver.find_element(By.XPATH,'//*[@id="xp__guests__inputs-container"]/div/div/div[1]/div/div[2]/button[1]')
            add_adult.click()

    def children(self,children_count=0,age1=0,age2=0,age3=0,age4=0,age5=0,age6=0,age7=0,age8=0,age9=0,age10=0):
        '''This function is used to define the number of children and their ages to be included in the search. Number of children restricted to 10.
            
            Attributes:
                children_count: int, the number of children to include in the search
                age(n): int, the age of each child where n is the number of children
            
            Example:
            ".children(2,4,12)" includes 2 children aged 4 and 12 on the search'''
        if children_count>0:
            child_ages=[age2+2,age3+2,age4+2,age5+2,age6+2,age7+2,age8+2,age9+2,age10+2]
            children=self.driver.find_element(By.XPATH,'//*[@id="xp__guests__inputs-container"]/div/div/div[2]/div/div[2]/button[2]')
            children.click()
            choose_age=self.driver.find_element(By.XPATH,f'//*[@id="xp__guests__inputs-container"]/div/div/div[3]/select/option[{age1+2}]')
            choose_age.click()

        if children_count>1:
            count =1
            for child in range(1,children_count):
                age=child_ages[count-1]
                count+=1
                print(age)
                children=self.driver.find_element(By.XPATH,'//*[@id="xp__guests__inputs-container"]/div/div/div[2]/div/div[2]/button[2]')
                children.click()
                choose_age=self.driver.find_element(By.XPATH,f'//*[@id="xp__guests__inputs-container"]/div/div/div[3]/select[{count}]/option[{age}]')
                choose_age.click()

    
    def rooms(self,number_of_rooms=1):
        '''This function is used to define the number of rooms to be included in the search
            
            Attributes:
                number_of_rooms: int, the number of rooms to include in the search'''
        if number_of_rooms > 1:
            while number_of_rooms !=1:
                add_room=self.driver.find_element(By.XPATH,'//*[@id="xp__guests__inputs-container"]/div/div/div[4]/div/div[2]/button[2]/span')
                add_room.click()
                number_of_rooms -= 1        

first_booking = BeginningStage()
first_booking.get_webpage()
first_booking.choose_option_1()
#first_booking.accept_cookies()
#first_booking.select_search_bar()
first_booking.choose_dates()
first_booking.adults(2)
#first_booking.children(2,4,14)
#first_booking.rooms(2)
first_booking.click_search_button()
# first_booking.duplicate_tab()
# first_booking.apply_star_rating(2)
# first_booking.budget_filters(25)
first_booking.get_hotel_urls()
first_booking.click_next_page()
#first_booking.get_hotel_details()
# first_booking.write_to_csv()