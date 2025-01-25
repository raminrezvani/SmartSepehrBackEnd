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
lst_date1=['23','24','25']

lst_date2=['26','27','28']
for date1,date2 in zip(lst_date1,lst_date2):

    try:
        driver.find_element(By.XPATH, '//div[@class="full-width date local"]').click()
    except:
        ''

    driver.find_element(By.XPATH, f'//div[contains(@class,"pdp-day") and @value="{date1}"]').click()

    driver.find_element(By.XPATH,f'//div[contains(@class,"pdp-day") and @value="{date2}"]').click()
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





