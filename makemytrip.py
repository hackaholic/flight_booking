__author__ = "Kumar Shubham"
import time
import datetime
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# Making loggin configuration
FORMAT = '%(asctime)-15s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='makemytrip.log', format=FORMAT, level=logging.INFO, datefmt='%Y-%m-%dT%H:%M:%S')
logger = logging.getLogger('makemytrip') 

class bookTrip:
    def __init__(self):
        logger.info("Initializing bookTrip class")
        self.browser = webdriver.Firefox(executable_path='./bin/geckodriver')
        self.baseurl = 'https://www.makemytrip.com/flights/'

    def datepicker(self, datefilter):
        logger.info("Selecting date for {}".format(datefilter))
        div = self.browser.find_element_by_xpath('//div[@class="{} hasDatepicker"]'.format(datefilter))
        first = div.find_element_by_xpath('./div/div[@class="ui-datepicker-group ui-datepicker-group-first"]')
        last = div.find_element_by_xpath('./div/div[@class="ui-datepicker-group ui-datepicker-group-last"]'.format(datefilter))
        return first, last

    def flight_search(self):
        logger.info("Starting to look for flights...")
        self.browser.get(self.baseurl)
        time.sleep(3)
        self.from_flight = self.browser.find_element_by_id("hp-widget__sfrom")
        self.to_flight = self.browser.find_element_by_id("hp-widget__sTo")
        self.from_flight.clear()
        self.to_flight.clear()
        self.from_flight.send_keys("Delhi")
        self.sleeptime(3)
        self.to_flight.send_keys("Bangalore")
        self.sleeptime(3)
        self.depart_time = self.browser.find_element_by_id("hp-widget__depart")
        self.return_time = self.browser.find_element_by_id("hp-widget__return")
        self.now = datetime.datetime.now()
        self.time_delta = datetime.timedelta(1)
        self.today = "{}000".format(int(datetime.datetime.strptime(datetime.datetime.strftime(self.now, "%d-%m-%y"), "%d-%m-%y").timestamp()))
        self.tomorrow = "{}000".format(int(datetime.datetime.strptime(datetime.datetime.strftime(self.now + self.time_delta, "%d-%m-%y"), "%d-%m-%y").timestamp()))
        self.depart_time.click()
        date_picker_first, date_picker_last = self.datepicker('dateFilter')
        xpath = './table/tbody/tr/td[@fare-date="{}"]'.format(self.today)
        date_picker_first.find_element_by_xpath(xpath).click()
        self.sleeptime(2)
        self.return_time.click()
        self.sleeptime(1)
        date_picker_first, date_picker_last = self.datepicker('dateFilterReturn')
        xpath = './table/tbody/tr/td[@fare-date="{}"]'.format(self.tomorrow)
        date_picker_first.find_element_by_xpath(xpath).click()
        logger.info("Form Populated for search, searching now...")
        self.browser.find_element_by_id('searchBtn').click()   

    def flight_booking(self):
        logger.info("Invoking flight_booking method")
        self.sleeptime(8)
        xpath = '//div[@class="clearfix"]'
        WebDriverWait(self.browser, 30).until(
            lambda x: x.find_element_by_xpath(xpath))
        logger.info("Searching for cheap flight ofr departure..")
        self.select_cheap('left')
        logger.info("Searching for cheap flight for return journey...")
        self.select_cheap('right')
        self.sleeptime(3)
        logger.info("Booking the flight now...")
        self.browser.find_element_by_xpath('//span[@class="stk_btm_earnpoint pull-right"]/span/a').click()
       
    def select_cheap(self, side):
        xpath = '//div[@class="clearfix"]/div[@class="col-xs-6 {}_pannel"]/div/div[@class="ng-scope"]/div/div/div[@class="ng-binding ng-scope"]'.format(side)
        scope = self.browser.find_elements_by_xpath(xpath)
        depart_price_min = 0
        depart_ele = ''
        for i,ele in enumerate(scope):
            xpath = './/div[@class="hidden-xs visible-stb clearfix"]/div[@class="price_info col-lg-3 col-md-3 col-sm-3 col-xs-3 text-right"]/p'
            price = int(ele.find_element_by_xpath(xpath).text.split()[-1].replace(',',''))
            if i == 0:
                depart_price_min = price
                depart_ele = ele
            if depart_price_min > price:
                depart_price_min = price
                depart_ele = ele
        depart_ele.click()

    def sleeptime(self,n):
        time.sleep(n)
        


def main():
    booktrip = bookTrip()
    booktrip.flight_search()
    booktrip.flight_booking()

if __name__ == '__main__':
    main()
