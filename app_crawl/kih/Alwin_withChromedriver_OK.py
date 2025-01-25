from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()

driver.get("https://www.allwin24.ir")
time.sleep(3)
import time

#======== search Source and Destination
first_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="online-tour"]'))
)
first_link.click()
# driver.find_element(By.XPATH,'//*[@id="online-tour"]').click()

first_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//div[@class="input-group"]//input'))
)
first_link.click()
# driver.find_element(By.XPATH,'//div[@class="input-group"]//input').click()

while(True):
    try:
        driver.find_element(By.XPATH,'//*[@id="online-tour"]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/ul/li[1]/a').find_element(By.XPATH,'//*[text()="خراسان رضوی"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="online-tour"]/div/div[2]/div[1]/div/div[1]/div[3]/div[2]/ul').find_element(By.XPATH,'.//*[text()="هرمزگان"]/..').click()
        break
    except:
        time.sleep(1)



#=== Search Date ==
lst_date1=['05/01','4/24','4/25','05/02']
lst_date2=['05/05','4/27','4/28','05/06']
import jdatetime
current=jdatetime.datetime.now()
current_month=current.month

for date1,date2 in zip(lst_date1,lst_date2):
    while(True):
        try:

            date1_month=int(date1.split('/')[0])
            if (date1_month==current_month):
                data1_column='0'
                iter1=0
            else:
                data1_column='1'
                iter1=-1

            date1_day=str(int(date1.split('/')[1]))

            date2_month=int(date2.split('/')[0])
            if (date2_month==current_month):
                data2_column='0'
                iter2=0
            else:
                data2_column='1'
                iter2=-1
            date2_day =str(int(date2.split('/')[1]))

            try:
                driver.find_element(By.XPATH, '//div[@class="full-width date local"]').click()
            except:
                ''
            first_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="برو به امروز"]'))
            )
            first_link.click()
            # driver.find_element(By.XPATH, '//button[text()="برو به امروز"]')


            driver.find_element(By.XPATH, f'//div[@data-column="{data1_column}"]').find_elements(By.XPATH,f'.//div[contains(@class,"pdp-day") and @value="{date1_day}"]')[iter1].click()
            # driver.find_element(By.XPATH, f'//div[contains(@class,"pdp-day") and @value="{date1}"]').click()

            # class="pdp-day"

            driver.find_element(By.XPATH, f'//div[@data-column="{data2_column}"]').find_elements(By.XPATH,f'//div[contains(@class,"pdp-day") and @value="{date2_day}"]')[iter2].click()
            # driver.find_element(By.XPATH,f'//div[contains(@class,"pdp-day") and @value="{date2}"]').click()



            driver.find_element(By.XPATH,f'//*[@id="online-tour"]/div/div[2]/div[4]/button').click()

            first_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="tour-hotel-result"]/div/div[2]/div[2]/div/div[2]/button'))
            )
            # first_link.click()
            time.sleep(5)

            try:
                driver.find_element(By.XPATH,'//div[@class="full-width date local"]').click()
            except:
                driver.find_element(By.XPATH, '//*[@id="fixResearch"]/div/div/div[2]/div/div/button').click()
                driver.find_element(By.XPATH, '//div[@class="full-width date local"]').click()

            break
        except:
            ''





