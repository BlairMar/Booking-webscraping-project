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


class Scraper():
    ''' This class is used to scrape data from Booking.com
    '''

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #options.add_argument("--headless")
        options.add_argument("--start-maximised")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # self.driver = webdriver.Chrome(options=options)
        self.hotel_urls = []
        self.dates=[] # Checkin and checkout dates to be saved as checkinyyyy, checkinmm, checkindd, checkoutyyyy, checkoutmm & checkoutdd
        self.dest=[]# Destiantion is saved in the list, however curretnly set to search only one destination
        self.travellers=[0,0,0,0,0,0,0,0,0,0,0,0]
        self.rooms = 0
        self.page_counter = 0
        self.s3_client = boto3.client('s3')
        self.start_url = 'https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggI46AdIM1gEaFCIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4Au2Q-owGwAIB0gIkMjgwYjc1OWMtNWJjNS00MzRmLTkwMzAtYzllNDk0OTc5ZWFh2AIE4AIB&lang=en-us&sid=61c3b046e3496364bf0e0cc43c757203&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaFCIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4Au2Q-owGwAIB0gIkMjgwYjc1OWMtNWJjNS00MzRmLTkwMzAtYzllNDk0OTc5ZWFh2AIE4AIB%3Bsid%3D61c3b046e3496364bf0e0cc43c757203%3Bsb_price_type%3Dtotal%3Bsig%3Dv1w_e9ye7_%26%3B&ss=Barcelona&is_ski_area=0&dest_type=city&checkin_year=2022&checkin_month=1&checkin_monthday=19&checkout_year=2022&checkout_month=1&checkout_monthday=20&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1'


    # def get_webpage(self):
    #     '''This function is used to fetch a webpage using ChromeDriver.
        
    #     Returns:
    #         webpage'''
    #     url = self.start_url
    #     webpage = self.driver.get(url)
    #     time.sleep(3)
    #     return webpage


    def get_webpage(self):
        '''This amends the URL to search for the user inputted data'''
        self.get_dates()
        self.get_dates()
        self.get_dest()
        self.get_travellers()
        self.get_rooms()
        
        curl = f'https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggI46AdIM1gEaFCIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4Au2Q-owGwAIB0gIkMjgwYjc1OWMtNWJjNS00MzRmLTkwMzAtYzllNDk0OTc5ZWFh2AIE4AIB&lang=en-us&sid=61c3b046e3496364bf0e0cc43c757203&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaFCIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4Au2Q-owGwAIB0gIkMjgwYjc1OWMtNWJjNS00MzRmLTkwMzAtYzllNDk0OTc5ZWFh2AIE4AIB%3Bsid%3D61c3b046e3496364bf0e0cc43c757203%3Bsb_price_type%3Dtotal%3Bsig%3Dv1w_e9ye7_%26%3B&ss={self.dest[0]}&is_ski_area=0&dest_type={self.dest[1]}&checkin_year={self.dates[0]}&checkin_month={self.dates[1]}&checkin_monthday={self.dates[2]}&checkout_year={self.dates[3]}&checkout_month={self.dates[4]}&checkout_monthday={self.dates[5]}&group_adults={self.travellers[0]}&group_children={self.travellers[1]}&age={self.travellers[2]}&age={self.travellers[3]}&age={self.travellers[4]}&age={self.travellers[5]}&age={self.travellers[6]}&age={self.travellers[7]}&age={self.travellers[8]}&age={self.travellers[9]}&age={self.travellers[10]}&age={self.travellers[11]}&no_rooms={self.rooms}&b_h4u_keep_filters=&from_sf=1'
        webpage = self.driver.get(curl)
        time.sleep(5)
        self.driver.get_screenshot_as_file("screenshot_post-get_webpage-headed.png")
        return webpage

        
    def accept_cookies(self):
        '''This function is used to click the 'accept cookies' button that appears on the webpage'''
        accept = self.driver.find_element(By.ID,'onetrust-accept-btn-handler')
        accept.click()
    
    def get_dates(self):
        travel_dt = input('Enter Travel date (yyyy-mm-dd): ')
        self.dates.append(travel_dt[0:4])
        self.dates.append(travel_dt[5:7])
        self.dates.append(travel_dt[8:10])
        return self.dates
        
    def get_dest(self):
        user_dest = input('Enter the desitnation of your choice : ')
        self.dest.append(user_dest)
        user_country = input('Is this a country? [Y/N]:')
        user_country = user_country.upper()
        if user_country == 'Y':
            self.dest.append('country')
        else:
            self.dest.append('city')
        return self.dest

    def get_travellers(self):
        '''This function is used to define the number of adults to be included in the search
            
            Attributes:
                adult_count: int, the number of adults to include in the search'''
        
        adults = int(input("How many adults are travelling? (max = 30): "))
        self.travellers[0] = adults
        children = int(input("How many children are travelling?(max = 10): "))
        self.travellers[1] = (children)

        if children == 1:
            children_age = int(input("Please input the child's age: "))
            self.travellers[2] = (children_age)
        elif children > 1:
            n = 1
            while n <= children:
                children_age = input(f"Please input the age of child {n}:  ")
                self.travellers[n+1] = (children_age)
                n += 1
        return self.travellers

   
    def get_rooms(self):
        '''This function is used to define the number of rooms to be included in the search
            
            Attributes:
                number_of_rooms: int, the number of rooms to include in the search'''

        self.rooms = int(input("How many rooms do you need?: "))
        return self.rooms

    def get_hotel_urls(self):
        '''This function is used to retrieve a list of hotel URLs from the search result container.
        
        Returns:
            list: list of hotel URLs'''
        time.sleep(5)
        self.driver.get_screenshot_as_file("screenshot_get_url-headed.png")
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
        #pages_remaining = True
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

    

booking = Scraper()
booking.get_webpage()
booking.get_hotel_urls()
booking.get_hotel_details()
booking.click_next_page()
