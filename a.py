from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import re
import json
import time

def extract_info(text):
    pattern = r'^(.*?)(\d{1,3}\.\d{3}\.\d{3})'

    match = re.search(pattern, text, re.DOTALL)
    if match:
        name = match.group(1).rstrip('\n')
        price = match.group(2)
        return [name, price]

def print_computer(names, prices, links):
    for name, price, link in zip(names, prices, links):
        print(name + ", " + str(price) + ", " + link)
    
def convert_price(price_txt):
    price_txt = re.sub(r"[^\d]", "", price_txt)
    if not re.search(r"\d", price_txt):
        return 0
    return int(price_txt)
    

def set_driver(url):
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    driver = webdriver.Chrome(options= option)
    driver.get(url)
    time.sleep(3)
    return driver

def fpt_crawler():
    url = "https://fptshop.com.vn/may-tinh-xach-tay"
    driver = set_driver(url)

    # click the show more button repeatly to load the entire content
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div/div[3]/div[2]/div[3]/div/div[3]/a'))).click()
        except TimeoutException:
            break
    # get the names, prices and links and store in json file
    raw_infos = driver.find_elements(By.CLASS_NAME, 'cdt-product__info')
    names = []
    prices = []
    links = []
    for raw_info in raw_infos:
        name, price = extract_info(raw_info.text) # extract name and price
        link = raw_info.find_element(By.TAG_NAME, 'a').get_attribute('href')
        names.append(name)
        prices.append(convert_price(price))
        links.append(link)
    # store to db with names, prices, links
    print_computer(names, prices, links)
    driver.close()


def pv_crawler():
    url = 'https://phongvu.vn/c/laptop'
    driver = set_driver(url)
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#__next > div > div > div > div > div:nth-child(4) > div:nth-child(2) > div > div.teko-col.teko-col-10.css-gr7r8o > div.teko-row.css-16rlp3f > div > div > div:nth-child(11)"))).click()
            names = []
            prices = []
            links = []
            # get names
            for element in driver.find_elements(By.CLASS_NAME, "css-1ybkowq"):
                names.append(element.find_element(By.TAG_NAME, 'h3').text)
            # get prices
            for element in driver.find_elements(By.CLASS_NAME, "css-1co26wt"):
                price = convert_price(element.find_element(By.TAG_NAME, 'div').text)
                prices.append(price)

            # get links
            for element in driver.find_elements(By.CLASS_NAME, "css-pxdb0j"):
                links.append(element.get_attribute('href'))
            
            # store to db with names, prices, links
            print_computer(names, prices, links)
            
        except TimeoutException():
            break
    driver.close()

def tgdd_crawler():
    url = "https://www.thegioididong.com/laptop-ldp"
    driver = set_driver(url)
    brands = driver.find_element(By.XPATH, "/html/body/div[7]/div")
    brand_urls = [brand.get_attribute('href') for brand in brands.find_elements(By.TAG_NAME, 'a')]
    for brand_url in brand_urls:
        driver.get(brand_url)
        time.sleep(3)
        productls_driver = driver.find_element(By.CLASS_NAME, "listproduct")
        names = []
        prices =[]
        links = []
        
        for element in productls_driver.find_elements(By.TAG_NAME, 'h3'):
            names.append(element.text)
        
        for element in productls_driver.find_elements(By.CLASS_NAME, "price"):
            prices.append(convert_price(element.text))
        
        for element in productls_driver.find_elements(By.CLASS_NAME, "main-contain"):
            links.append(element.get_attribute('href'))

        # store to db with names, prices, links
        print_computer(names, prices, links)
    driver.close()

def cp_crawler():
    url = "https://cellphones.com.vn/laptop.html"
    driver = set_driver(url)
    brands = driver.find_element(By.CLASS_NAME, "list-brand")
    brand_urls = [brand.get_attribute('href') for brand in brands.find_elements(By.TAG_NAME, 'a')]    
    for brand_url in brand_urls:
        driver.get(brand_url)
        time.sleep(3)
        while True:
            try:
                computer_infos = driver.find_elements(By.CLASS_NAME, "product-info")
                names = []
                prices =[]
                links = []
                
                for computer_info in computer_infos:
                    names.append(computer_info.find_element(By.TAG_NAME, 'h3').text)
                    price = convert_price(computer_info.find_element(By.CLASS_NAME, "product__price--show").text)
                    if price != 0:
                        prices.append(price)
                    links.append(computer_info.find_element(By.TAG_NAME, 'a').get_attribute('href'))

                # store to db with names, prices, links
                print_computer(names, prices, links)
                
                #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > div.block-filter-sort > div.filter-sort__list-product > div > div.cps-block-content_btn-showmore > a > div > svg"))).click()
            except TimeoutException():
                break

if __name__ == "__main__":
    # fpt_crawler()
     pv_crawler()
    # tgdd_crawler()
    # cp_crawler()
    
