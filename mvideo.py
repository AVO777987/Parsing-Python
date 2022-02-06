from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

client = MongoClient('127.0.0.1', 27017)
db = client['database']
mvideo_bd = db.mvideo

driver = webdriver.Chrome(executable_path='./chromedriver')
driver.maximize_window()
driver.implicitly_wait(3)
driver.get('https://www.mvideo.ru/')
elem = driver.find_element(By.TAG_NAME, "body")
while True:
    try:
        elem = driver.find_element(By.XPATH, "//span[contains(text(), 'В тренде')]")
        elem.click()
        break
    except:
        elem.send_keys(Keys.PAGE_DOWN)
prices = []
elem = driver.find_elements(By.XPATH, "//mvid-carousel[contains(@class, 'carusel')]")[0]
elems = elem.find_elements(By.XPATH, ".//span[@class='price__main-value']")
for el in elems:
    prices.append(''.join(el.text.split()))

elems = elem.find_elements(By.XPATH, ".//a[contains(@class, 'img-with-badge')]")
product_item = 0
for el in elems:
    product = {}
    product['url'] = el.get_attribute('href')
    product['name'] = el.find_element(By.TAG_NAME, "img").get_attribute('alt')
    img_src = el.find_element(By.TAG_NAME, "img").get_attribute("srcset").split(',', )
    for i in range(len(img_src)):
        img_src[i] = f'https:{img_src[i].replace(" ", "").replace("50w", "").replace("65w", "").replace("480w", "").replace("95w", "").replace("200w", "").replace("80w", "").replace("600w", "")}'
    product['img_src'] = img_src
    product['price'] = prices[product_item]
    product_item += 1
    mvideo_bd.insert_one(product)
