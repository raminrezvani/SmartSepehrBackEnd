#https://anti-captcha.com/fa/clients/reports/tasks
#https://anti-captcha.com/

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
#----------- Get and Download Captua -------
def get_image_src():
    driver=webdriver.Chrome()
    driver.get('https://mehraginseir.ir/Systems/Login.aspx?language=fa')
    src=driver.find_element(By.ID,'imgCaptcha').get_property('src')
    return src

def download_image(src,filename):
    # Local filename to save the image
    # filename = "mehraginseir.jpg"
    # Send a GET request to the URL
    response = requests.get(src, stream=True)
    response.raise_for_status()  # Raise an exception for HTTP errors
    with open(filename, "wb") as file:
        for chunk in response.iter_content(1024):  # Download in chunks
            file.write(chunk)

#-------



from anticaptchaofficial.imagecaptcha import *
def get_resolvedCaptua(filename):
    api_key='2bd2e13190002d384511fc3815e69724'
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_soft_id(0)
    solver.set_language_pool("rn")
    captcha_text = solver.solve_and_return_solution(filename)
    if captcha_text != 0:
        print ("captcha text "+captcha_text)
    else:
        print ("task finished with error "+solver.error_code)
    return captcha_text


#---------
# src=get_image_src()
# filename="mehraginseir.jpg"
# download_image(src,filename)
# captcha_text=get_resolvedCaptua(filename)
# print(captcha_text)