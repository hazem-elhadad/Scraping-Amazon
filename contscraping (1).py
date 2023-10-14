from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import csv
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
URLS=[]
df=pd.read_csv('Input.csv')
df1=pd.read_csv('Output.csv')
last_scraped=len(df1['URL'])
file = open('Output.csv', 'a', encoding='utf-8', newline='')
csv_writer = csv.writer(file)
csv_writer.writerow(['Title', 'Brand', 'Price' ,'Prime' , 'URL'])
def passingerror():
    while True:
        try:
            attrr = driver.find_element(By.XPATH ,'//div[@id="g"]/div/a/img').get_attribute("alt")
            if "Sorry! Something went wrong" in attrr:
                driver.refresh()
                sleep(1)
        except:
            break
def changeAdress():
    driver.get("https://www.amazon.com/usa/s")
    passingerror()
    x = 0
    z = 0
    while True:
        try:
            try:
                driver.maximize_window()
                driver.find_element(By.XPATH, '//span[@id="glow-ingress-line2"]').click()
                sleep(1)
                driver.find_element(By.XPATH, '//input[@aria-label="or enter a US zip code"]').send_keys(78250)
                sleep(1)
                driver.find_element(By.XPATH, '//div[@class="a-column a-span4 a-span-last"]').find_element(By.XPATH,
                                                                                                           '//input[@aria-labelledby="GLUXZipUpdate-announce"]').click()
                driver.refresh()
            except:
                pass
            if "San" in driver.find_element(By.ID, 'glow-ingress-line2').text:
                print("all good")
                break
            z += 1
            if z == 5: break
        except:
            print("Location not changed yet")
            sleep(2)
            x += 1
            if x == 3:
                print("try again location error")
                break
changeAdress()
def scrapetitle():
    title='No'
    try:
        title = driver.find_element(By.XPATH, '//div[@id="titleSection"]').find_element(By.ID, 'title').find_element(
            By.ID, 'productTitle').text
    except:
        pass
    return title
def scrapebrand():
    brand="No"
    try:
        branddata = driver.find_element(By.XPATH, '//div[@id="productOverview_feature_div"]').find_element(
            By.CLASS_NAME, 'a-section.a-spacing-small.a-spacing-top-small').find_element(By.CLASS_NAME,
                                                                                         'a-normal.a-spacing-micro').find_element(
            By.TAG_NAME, 'tbody').find_element(By.CLASS_NAME, 'a-spacing-small.po-brand').find_elements(By.TAG_NAME,
                                                                                                        'td')
        brand = branddata[1].text
    except:
        pass
    return brand
def scrapeprice():
    price ="No"
    try:
        divs = driver.find_element(By.XPATH, '//div[@id="corePrice_desktop"]').find_elements(By.TAG_NAME, 'span')
        for onediv in divs:
            if onediv.get_attribute("class") == "a-price a-text-price a-size-medium apexPriceToPay":
                price = onediv.text
                break
    except:
        pass
    try:
        if "$" not in price:
            price = (driver.find_element(By.XPATH, '//span[@id="sns-base-price"]').text).rsplit("(", 1)[0]
    except:
        pass
    try:
        if "$" not in price:
            price = (driver.find_element(By.XPATH,
                                         '//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]').text).replace(
                '\n', ',')
    except:
        pass
    try:
        if "$" not in price:
            price = (driver.find_element(By.XPATH, '//span[@id="size_name_1_price"]').text).split('\n')[1]
    except:
        pass
    return price
def scrapeprime():
    prime="No"
    try:
        if driver.find_element(By.XPATH, '//div[@id="bbop-content-container"]'):
            prime = "yes"
    except:
        pass
    return prime
pronum=0
for productlink in df['URL'][last_scraped:]:
    print(f"Scraping product number {last_scraped}")
    pronum+=1
    last_scraped+=1
    # if pronum == 10:break
    driver.get(productlink)
    passingerror()
    try:
        if driver.find_element(By.XPATH ,'//div[@id="titleSection"]'):
            try:
                Title=scrapetitle()
                Brand=scrapebrand()
                Price=scrapeprice()
                Prime=scrapeprime()
            except:
                print("Revise Scrape Function")
                pass
    except:
        print("Url error")
        pass
    csv_writer.writerow([Title,Brand,Price,Prime, productlink])
file.close()


