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
import boto3
import json
import math
import psycopg2
from sqlalchemy import create_engine
import aws_session


class Scraper():
    ''' This class is used to scrape data from Booking.com
    '''

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'")
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.hotel_urls = []
        self.dates=[] # Checkin and checkout dates to be saved as checkinyyyy, checkinmm, checkindd, checkoutyyyy, checkoutmm & checkoutdd
        self.dest=[]# Destiantion is saved in the list, however curretnly set to search only one destination
        self.travellers=[0,0,0,0,0,0,0,0,0,0,0,0]
        self.rooms = 0
        self.page_counter = 0
        self.s3_client = aws_session.session.client('s3')
        self.s3_resource = aws_session.session.resource('s3')
        self.end_url = None
        self.hotel_count = 0
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT = 'bookingscraperdb.crrotzprrmrr.us-east-2.rds.amazonaws.com'
        USER = 'postgres'
        PASSWORD = 'r8wsxVceuncMNT8'
        DATABASE = 'postgres'
        PORT = 5432
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")

    def get_webpage(self):
        '''This amends the URL to search for the user inputted data'''
        self.get_dates()
        self.get_dates()
        self.get_dest()
        self.get_travellers()
        self.get_rooms()
        
        self.end_url = f'https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggI46AdIM1gEaFCIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4Au2Q-owGwAIB0gIkMjgwYjc1OWMtNWJjNS00MzRmLTkwMzAtYzllNDk0OTc5ZWFh2AIE4AIB&lang=en-us&sid=61c3b046e3496364bf0e0cc43c757203&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaFCIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4Au2Q-owGwAIB0gIkMjgwYjc1OWMtNWJjNS00MzRmLTkwMzAtYzllNDk0OTc5ZWFh2AIE4AIB%3Bsid%3D61c3b046e3496364bf0e0cc43c757203%3Bsb_price_type%3Dtotal%3Bsig%3Dv1w_e9ye7_%26%3B&ss={self.dest[0]}&is_ski_area=0&dest_type={self.dest[1]}&checkin_year={self.dates[0]}&checkin_month={self.dates[1]}&checkin_monthday={self.dates[2]}&checkout_year={self.dates[3]}&checkout_month={self.dates[4]}&checkout_monthday={self.dates[5]}&group_adults={self.travellers[0]}&group_children={self.travellers[1]}&age={self.travellers[2]}&age={self.travellers[3]}&age={self.travellers[4]}&age={self.travellers[5]}&age={self.travellers[6]}&age={self.travellers[7]}&age={self.travellers[8]}&age={self.travellers[9]}&age={self.travellers[10]}&age={self.travellers[11]}&no_rooms={self.rooms}&b_h4u_keep_filters=&from_sf=1'
        webpage = self.driver.get(self.end_url)
        hotel_count_text = self.driver.find_element(By.XPATH,'//*[@id="right"]/div[1]/div/div/div/h1').text
        hotel_count_text = hotel_count_text.split(": ")
        hotel_count_text = hotel_count_text[1].split(" p")
        hotel_count_text = hotel_count_text[0].replace(",","")
        self.hotel_count = int(float(hotel_count_text))
        print(f'{self.hotel_count} hotels found')
        return webpage
    
    def get_dates(self):
        '''This method retrieves the travel dates from user input.
            Returns: 
                self.dates - list of travel dates'''

        try:
            travel_dt = input('Enter Travel date (yyyy-mm-dd): ')
            self.dates.append(travel_dt[0:4])
            self.dates.append(travel_dt[5:7])
            self.dates.append(travel_dt[8:10])
        except:
            print('')
            print('No user input detected, using default values (Departure 1st Jan 2022, Return 10th Jan 2022)')
            self.dates = ['2022','01','01','2022','01','10']
        return self.dates
        
    def get_dest(self):
        '''This method retrieves the travel destination name and type from user input.
            Returns: 
                self.dest - list of travel destination and country or city'''
        try:
            user_dest = input('Enter the desitnation of your choice : ')
            self.dest.append(user_dest)
            user_country = input('Is this a country? [Y/N]:')
            user_country = user_country.upper()
            if user_country == 'Y':
                self.dest.append('country')
            else:
                self.dest.append('city')  
        except:
            print('')
            print('No user input detected, using default value (Spain)')
            self.dest = ['spain','country']
        return self.dest

    def get_travellers(self):
        '''This function is used to retrieve the number of travellers from user input.
            
            Returns:
                self.travellers - list of number of adults, number of children and their ages'''

        try:
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
        except:
            print('')
            print('No user input detected, using default values (2 adults, 0 children)')
            self.travellers = [2,0,0,0,0,0,0,0,0,0,0,0]
        return self.travellers

   
    def get_rooms(self):
        '''This function is used to retrieve the number of rooms from user input.
            
            Returns:
                self.rooms - int'''
        try:
            self.rooms = int(input("How many rooms do you need?: "))
        except:
            print('')
            print('No user input detected, using default value (1 room)')
            self.rooms = 1
        return self.rooms

    def get_hotel_urls(self):
        '''This function is used to retrieve a list of hotel URLs from the search result container.
        
        Returns:
            list: list of hotel URLs'''
        time.sleep(5)
        hotel_container = self.driver.find_element(By.ID,'search_results_table')
        hotel_list = hotel_container.find_elements(By.CSS_SELECTOR,'div[data-testid="property-card"]')

        
        for element in hotel_list:
            hotel_url = element.find_element(By.XPATH,'.//a')
            hotel_url = hotel_url.get_attribute('href')
            self.hotel_urls.append(hotel_url)
        self.page_counter += 1
        print(f'Pages visited: {self.page_counter}')
        print(len(self.hotel_urls))

    def get_hotel_details(self):
        '''This function is used to retrieve individual hotel details.

            Returns:
                list: list of dictionaries containing individual hotel details '''
        print('gathering hotel data')
        hotel_detail_dict_list = []

        for i, url in enumerate(self.hotel_urls):
            hotel_detail_dict = {'Name' : None, 'Room_Type': None ,'Price' : None, 'Address': None, 'Deals': None, 
                            'Wifi' : 0,'Rating' : None,'Facilities' : None, 'Star': None}
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
            
            # For some reason I am unable to get the stars part working.
            try:    
                hotel_stars  = self.driver.find_element(By.XPATH,'//*[@id="wrap-hotelpage-top"]/div[1]/span/span[1]/div/div/span/div/span')
                hotel_detail_dict['Star'] = hotel_stars.text  
            except:
                hotel_detail_dict['Star'] = 'Stars unavailable'   
                           
            
            hotel_detail_dict_list.append(hotel_detail_dict)
            s3object = self.s3_resource.Object('bookingbucket', f'hotel_jsons/hotel{i+1}.json')
            s3object.put(Body=(bytes(json.dumps(hotel_detail_dict).encode('UTF-8'))))
            
        print('gathered all hotel data')
        df = pd.json_normalize(hotel_detail_dict_list) 
        df.to_csv('hotels.csv')
        df.to_sql('hotels',self.engine,if_exists = 'replace')
        self.driver.quit()
        self.s3_client.upload_file('hotels.csv', 'bookingbucket', 'hotels.csv')
    

    def click_next_page(self):
        '''This function is used to click the next page of search results'''
        offset = 25
        page_max = math.ceil(self.hotel_count/25)
        pages = 120
        max_offset = (page_max -1) * 25
       
        # ##USE TO SCRAPE ALL PAGES
        # while offset < max_offset:
        #     next_page = self.end_url + f'&offset={offset}'
        #     self.driver.get(next_page)
        #     offset += 25
        #     self.get_hotel_urls()

        ##USE TO SCRAPE SMALL RANGE (FOR TESTING) - note each page = 25 results, 2 pages = 50 etc. while offset < 50; scrapes 2 pages
        while offset < (pages*25):
            next_page = self.end_url + f'&offset={offset}'
            self.driver.get(next_page)
            offset += 25
            self.get_hotel_urls()


booking = Scraper()
booking.get_webpage()
booking.get_hotel_urls()
booking.click_next_page()
booking.get_hotel_details()
