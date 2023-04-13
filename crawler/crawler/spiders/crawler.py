from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re
from scrapy.selector import Selector
import scrapy



class FptShopSpider(scrapy.Spider):
    name = 'fptshop'
    allowed_domains = ['https://fptshop.com.vn']
    start_urls = ['https://fptshop.com.vn/may-tinh-xach-tay']
    
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.option.add_argument("--incognito")
        self.browser = webdriver.Chrome(options=self.option)
        super(FptShopSpider, self).__init__()
    
    
    def convert_price(self, price_txt):
        price_txt = re.sub(r"[^\d]", "", price_txt)
        if not re.search(r"\d", price_txt):
            return 0
        return int(price_txt)
   
    def extract_info(self, text):
        pattern = r'^(.*?)(\d{1,3}\.\d{3}\.\d{3})'

        match = re.search(pattern, text, re.DOTALL)
        if match:
            name = match.group(1).rstrip('\n')
            price = match.group(2)
            return [name, price]

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5)
    # click the show more button repeatly to load the entire content
        while True:
            try:
                show_more_button = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div/div[3]/div[2]/div[3]/div/div[3]/a')))
                show_more_button.click()
            except TimeoutException:
                break

    # parse the loaded content
        try:
            raw_infos = self.browser.find_elements(By.CLASS_NAME, 'cdt-product__info')
            for raw_info in raw_infos:
                name, price = self.extract_info(raw_info.text) # extract name and price
                link = raw_info.find_element(By.TAG_NAME, 'a').get_attribute('href')
                # yield{
                #     'website': 'fpt',
                #     'name': name,
                #     'price': self.convert_price(price),
                #     'link': link
                # }
        except Exception as e:
            print(str(e))

    def closed(self, reason):
        self.browser.quit()


class TgddSpider(scrapy.Spider):
    name = 'tgdd'
    allowed_domains = ['https://www.thegioididong.com']
    start_urls = ['https://www.thegioididong.com/laptop-ldp']

    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.option.add_argument("--incognito")
        self.browser = webdriver.Chrome(options=self.option)
        super(TgddSpider, self).__init__()
    
    def convert_price(self, price_txt):
        price_txt = re.sub(r"[^\d]", "", price_txt)
        if not re.search(r"\d", price_txt):
            return 0
        return int(price_txt)
    def parse(self, response):
        self.browser.get(response.url)
        brands = self.browser.find_element(By.XPATH, "/html/body/div[7]/div")
        brand_urls = [brand.get_attribute('href') for brand in brands.find_elements(By.TAG_NAME, 'a')]
        for brand_url in brand_urls:
            self.browser.get(brand_url)
            time.sleep(3)
            productls_driver = self.browser.find_element(By.CLASS_NAME, "listproduct")
            
            names = []
            prices =[]
            links = []
        
            for element in productls_driver.find_elements(By.TAG_NAME, 'h3'):
                names.append(element.text)
        
            for element in productls_driver.find_elements(By.CLASS_NAME, "price"):
                prices.append(self.convert_price(element.text))
        
            for element in productls_driver.find_elements(By.CLASS_NAME, "main-contain"):
                links.append(element.get_attribute('href'))

            # for i in range(len(names)):
            #     yield {
            #         'website': 'tgdd',
            #         'name': names[i],
            #         'price': prices[i],
            #         'link': links[i]
            #     }
            
    def closed(self, reason):
        self.browser.quit()


class DienMayXanhSpider(scrapy.Spider):
    name = 'dienmayxanh'
    allowed_domains = ['https://www.dienmayxanh.com']
    start_urls = ['https://www.dienmayxanh.com/laptop']
    
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.option.add_argument("--incognito")
        self.browser = webdriver.Chrome(options=self.option)
        super(DienMayXanhSpider, self).__init__()
    
    
    def convert_price(self, price_txt):
        price_txt = re.sub(r"[^\d]", "", price_txt)
        if not re.search(r"\d", price_txt):
            return 0
        return int(price_txt)
   
    def extract_info(self, text):
        name_pattern = r'^(.+)\nRAM'
        name_match = re.search(name_pattern, text, re.MULTILINE)
        name = name_match.group(1)

        price_pattern = r"(\d[\d\.]*)₫"
        prices_match = re.findall(price_pattern, text)
        
        price = 0
        if len(prices_match) == 1:
            price = prices_match[0]
        else:
            price = prices_match[len(prices_match) - 2]
        price = self.convert_price(price)

        return [name, price]

    def parse(self, response):
        self.browser.get(response.url)
    # click the show more button repeatly to load the entire content
        while True:
            try:
                show_more_button = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="cate-main-container"]/section/div[3]/div[2]/a')))
                show_more_button.click()
                time.sleep(3)
            except TimeoutException:
                break
    # parse the loaded content
        try:
             raw_infos = self.browser.find_elements(By.CSS_SELECTOR, ".item.__cate_44")
             for raw_info in raw_infos:
                name, price = self.extract_info(raw_info.text)
                link = raw_info.find_element(By.TAG_NAME, 'a').get_attribute('href')

                # yield{
                #     'website': 'dienmayxanh',
                #     'name': name,
                #     'price': self.convert_price(price),
                #     'link': link
                # }
        except Exception as e:
             print(str(e))

    def closed(self, reason):
        self.browser.quit()


class  HoangHaMobileSpider(scrapy.Spider):
    name = 'hoanghamobile'
    allowed_domains = ['https://hoanghamobile.com']
    start_urls = ['https://hoanghamobile.com/laptop']
    
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--disable-extensions')
        self.option.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.option.add_argument("--incognito")
        self.browser = webdriver.Chrome(options=self.option)
        super(HoangHaMobileSpider, self).__init__()
    
    def extract_info(self, text):
        name_pattern = r"Laptop\s(.+?)\n"
        price_pattern = r"(\d{1,3}\,\d{3}\,\d{3})"
        name_match = re.search(name_pattern, text)
        price_matches = re.findall(price_pattern, text)
        name = name_match.group(1)
        name = name.split(" - ")[0]
        price = self.convert_price(price_matches[0])
        return [name, price]

    def convert_price(self, price_txt):
        price_txt = re.sub(r"[^\d]", "", price_txt)
        if not re.search(r"\d", price_txt):
            return 0
        return int(price_txt)

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5)

        #close pop-ups
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.close-modal.icon-minutes'))).click()
    
    # click the show more button repeatly to load the entire content
        # while True:
        #     try:
        #         show_more_button = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="container"]/div[2]/a')))
        #         show_more_button.click()
        #         time.sleep(3)
        #     except TimeoutException:
        #         break
    # parse the loaded content
    
        try:
             content = self.browser.find_element(By.CSS_SELECTOR, ".col-content.lts-product")
             raw_infos = content.find_elements(By.CLASS_NAME, 'item')
             for raw_info in raw_infos:
                name, price = self.extract_info(raw_info.text)
                link = raw_info.find_element(By.CLASS_NAME, 'info').find_element(By.TAG_NAME, 'a').get_attribute('href')

                # yield{
                #     'website': 'hoanghamobile',
                #     'name': name,
                #     'price': self.convert_price(price),
                #     'link': link
                # }
        except Exception as e:
             print(str(e))

    def closed(self, reason):
        self.browser.quit()




