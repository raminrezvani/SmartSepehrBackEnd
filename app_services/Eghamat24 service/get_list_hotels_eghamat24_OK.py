from selenium import webdriver
from selenium.webdriver.common.by import By



#================== Read for each property_id ============
driver=webdriver.Chrome()

def get_stars(city):
    import json
    with open(f'eghamat_data/lstHotels_{city}.json', 'r', encoding='utf-8') as file:
        lst_items_ok = json.load(file)

    for item in lst_items_ok:
        try:
            driver.get(item['href'])
            value=driver.find_element(By.XPATH,'//input[@name="property_id"]').get_attribute('value')
            item['property_id']=value

            hotel_grid=driver.find_element(By.XPATH,'//span[@class="hotel_grid"]').text.replace('(','').replace(')','').replace('هتل','').replace('ستاره','').strip()
            if ( 'یک' in hotel_grid):
                hotel_grid='1'
            elif ( 'دو' in hotel_grid):
                hotel_grid='2'
            elif ( 'سه' in hotel_grid):
                hotel_grid='3'
            elif ( 'چهار' in hotel_grid):
                hotel_grid='4'
            elif ( 'پنج' in hotel_grid):
                hotel_grid='5'
            else:
                hotel_grid=''
        except:
            hotel_grid='3'

        item['star'] = hotel_grid

    import json
    with open(f'eghamat_data/lstHotels_{city}_withProperty.json', 'w', encoding='utf-8') as file:
        json.dump(lst_items_ok, file, ensure_ascii=False)



#================================
# 'AWZ': {},
# 'BND': {},
# 'ZBR': {},
# 'KER': {},
# 'KSH': {},
# 'RAS': {},
# 'SRY': {},

# city='BND'
# get_stars('BND')
# get_stars('ZBR')
# get_stars('KER')
# get_stars('KSH')
# get_stars('RAS')
# get_stars('SRY')

# get_stars('ABD')
# get_stars('BUZ')
# get_stars('GBT')
# get_stars('OMH')
get_stars('ADU')
# get_stars('HDM')
# get_stars('RZR')
# get_stars('KHD')



#=======================================================
# 'KIH': {},
# 'GSM': {},
# 'MHD': {},
# 'SYZ': {},
# 'THR': {},
# 'IFN': {},
# 'AZD': {},
# 'TBZ': {},
#
# 'AWZ': {},
# 'BND': {},
# 'ZBR': {},
# 'KER': {},
# 'KSH': {},
# 'RAS': {},
# 'SRY': {},
#==== =========

driver=webdriver.Chrome()
# driver.get('https://www.eghamat24.com/AhvazHotels.html')
# driver.get('https://www.eghamat24.com/BandareabbasHotels.html')
# driver.get('https://www.eghamat24.com/ChabaharHotels.html')
# driver.get('https://www.eghamat24.com/KermanHotels.html')
# driver.get('https://www.eghamat24.com/KermanshahHotels.html')
# driver.get('https://www.eghamat24.com/RashtHotels.html')
# driver.get('https://www.eghamat24.com/SariHotels.html')

#=============
# driver.get('https://www.eghamat24.com/AbadanHotels.html')
# city='ABD'
# # #---
# driver.get('https://www.eghamat24.com/BushehrHotels.html')
# city='BUZ'
#
# driver.get('https://www.eghamat24.com/GorganHotels.html')
# city='GBT'
#
# driver.get('https://www.eghamat24.com/UrmiaHotels.html')
# city='OMH'
#
# driver.get('https://www.eghamat24.com/ArdabilHotels.html')
# city='ADU'
# #
#
# driver.get('https://www.eghamat24.com/HamedanHotels.html')
# city='HDM'
#
#
# driver.get('https://www.eghamat24.com/RamsarHotels.html')
# city='RZR'
#
#
# driver.get('https://www.eghamat24.com/KhorramabadHotels.html')
# city='KHD'




lst_unique_href=list()
lst_items=[
    {
        'title':a.get_attribute('title'),
        'href':a.get_attribute('href')
    }
    for a in driver.find_elements(By.XPATH,'//article[@class="property-card-vertical"]//a')]

lst_items_ok=list()
for item in lst_items:
    if item['href'] not in lst_unique_href:
        lst_unique_href.append(item['href'])
        lst_items_ok.append(item)


import json
with open(f'eghamat_data/lstHotels_{city}.json', 'w', encoding='utf-8') as file:
    json.dump(lst_items_ok, file, ensure_ascii=False)
#=== Read ===
# import json
# with open('output.json', 'r', encoding='utf-8') as file:
#     lst_items_ok = json.load(file)

print('asd')

#==============