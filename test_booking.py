import unittest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from Booking.booking import BeginningStage

class BeginnerStageTestCase(unittest.TestCase):
    def setUp(self):
        self.test = BeginningStage()

    def test_choose_option_1_1(self):
        self.test.get_webpage()
        self.test.accept_cookies()
        option_1 = self.test.choose_option_1()
        self.assertIsNone(option_1)

    def test_select_search_bar(self):  
        self.test.get_webpage()
        self.test.accept_cookies()
        self.test.choose_option_1()
        self.user_destination = input('What is your destination? :')
        test_user_destination = self.test.select_search_bar()
        self.assertEqual(test_user_destination, self.user_destination)

    def test_choose_dates(self):
        self.test.get_webpage()
        self.test.accept_cookies()
        self.test.choose_option_1()
        self.test.select_search_bar()
        dates_chosen = self.test.choose_dates()
        self.assertIsNone(dates_chosen)

if __name__ == '__main__':
    unittest.main(argv=[' '], verbosity=2, exit=False)


    
    