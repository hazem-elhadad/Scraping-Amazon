#import statments
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
import csv
file=open('Input.csv','w',encoding='utf-8',newline='')
csv_writer=csv.writer(file)
csv_writer.writerow(['Asin Number' , 'URL'])
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
page = 0
Asins_list = []
Asins_links=[]
Links_list=[]
#الجزء ده بنحط اللينك بتاع ال category الى عايزين نسحب الداتا بتاع المنتجات بتاعته في فايل text انا عامله ف المشروع
f = open("CategoryURL.txt", "r", encoding="utf8")
URL = f.readlines()
url = URL[0].strip()
driver.get(url)
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
                try:
                    driver.find_element(By.XPATH, '//span[@id="glow-ingress-line2"]').click()
                except:driver.find_element(By.XPATH ,'//input[@data-action-type="SELECT_LOCATION"]').click()
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
while True:
    page+=1
    url_parts = url.split("page=")
    finaleURl = url_parts[0] + "page=" + str(page) + (url_parts[1])[1:-1] + str(page)
    driver.get(finaleURl)
    passingerror()
    Asins = driver.find_element(By.XPATH ,'//div[@class="s-main-slot s-result-list s-search-results sg-row"]').find_elements(By.XPATH,'./div')
    for element1 in Asins:
        try:
            asin=element1.get_attribute('data-asin')
            if "B" in asin and asin not in Asins_list:
                productlink = element1.find_element(By.CLASS_NAME ,"a-link-normal.s-no-outline").get_attribute('href')
                Asins_list.append(asin)
                Links_list.append(productlink)
                # the_asin = "https://www.amazon.com/dp/" + (str(asin)).strip()
                # Asins_links.append(the_asin)
                csv_writer.writerow([asin, productlink])
        except:pass
    print(f"Page: {page}")
    # if page == 5:
    #    break
    try:
        driver.find_element(By.XPATH,'//span[@class="s-pagination-item s-pagination-next s-pagination-disabled "]')
        break
    except:pass
file.close()
# بنسحب اللينكات بتاعة المنتجات ونحطها في فايل csv عشان هنستخدمها تانى في اننا ندخل علي كل منتج ونسحب الداتا بتاعته

# المشروع عبارة عن Automation + Web scraping
# هيخلص ونرجع تانى
# خلصنا وهنعمل اسكريبت سحب المنتجات من كل لينك