# -*- coding: utf-8 -*-
#=============================================================================
#title           :upload.py
#description     :This automation script for. upload images on redbubble.com
#author          :Rajinder Sharma
#date            :16-02-2018
#version         :1.0
#usage           :upload.py
#notes           :
#python_version  :2.7  
#=============================================================================
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time, os, json, threading
# import pywinauto
def get_driver():
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome('C:/Users/dell/Downloads/chromedriver_win32/chromedriver.exe', chrome_options=options)
    #driver = webdriver.Chrome("C:/Users/dell/Downloads/chromedriver_win32/chromedriver.exe")
    return driver

def handle_dialog(element_initiating_dialog, dialog_text_input, driver):
    def _handle_dialog(_element_initiating_dialog):
        _element_initiating_dialog.click() # thread hangs here until upload dialog closes
    t = threading.Thread(target=_handle_dialog, args=[element_initiating_dialog] )
    t.start()
    time.sleep(1) # poor thread synchronization, but good enough

    upload_dialog = driver.switch_to_active_element()
    upload_dialog.send_keys(dialog_text_input)
    upload_dialog.send_keys(Keys.ENTER)

def image_upload(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(10)
    #open sign in popup and fill the email and password
    driver.find_element_by_xpath("//div[@id='RB_React_Component_LoginLink_4']//a[text()='Log In']").click()
    email_edit = driver.find_element_by_xpath('//*[@id="ReduxFormInput4"]')
    pw_edit = driver.find_element_by_xpath('//*[@id="ReduxFormInput5"]')
    login_button = driver.find_element_by_xpath('//*[@class="app-ui-components-Button-Button_button_1_MpP app-ui-components-Button-Button_primary_pyjm6 app-ui-components-Button-Button_padded_1fH5b"]')
    if email_edit and pw_edit and login_button:
        email_edit.click()
        email_edit.send_keys("rajinder323@gmail.com")
        time.sleep(1)
        pw_edit.click()
        pw_edit.send_keys("@987654321")
        time.sleep(1)
        pw_edit.submit()
        
        time.sleep(10)
    

    driver.get("https://www.redbubble.com/portfolio/images/new?ref=account-nav-dropdown")
    
    # upload art work image
    folder = os.getcwd()+"/image/"
    files_path = [folder + x for x in os.listdir(folder)]
    imagelist = []
    textlist = []
    for file in files_path:
        filename, file_extension = os.path.splitext(file)
        if file_extension.lower() != '.txt':
            imagelist.append(file)
        else:
            textlist.append(file)
    for image_path in imagelist:
        path = image_path
        time.sleep(2)
        #upload artwork image
        elm = driver.find_element_by_xpath("//input[@type='file'][@id='select-image-single']")
        elm.send_keys(path)
        time.sleep(20)
        # Fill the data in new artwork form
        art_title = driver.find_element_by_xpath('//*[@id="work_title_en"]')
        art_desc = driver.find_element_by_xpath('//*[@id="work_description_en"]')
        art_tag = driver.find_element_by_xpath('//*[@id="work_tag_field_en"]')
        art_is_mature = driver.find_element_by_xpath('//*[@id="work_safe_for_work_true"]')
        art_rights = driver.find_element_by_xpath('//*[@id="rightsDeclaration"]')
        save_button = driver.find_element_by_xpath('//*[@id="submit-work"]')
    
        
        if art_is_mature and art_rights:
            art_title.click()
            art_title.send_keys("My First Artwork")
            time.sleep(1)
            art_desc.click()
            art_desc.send_keys("This is my first beautiful artwork")
            time.sleep(1)
            art_tag.click()
            art_tag.send_keys("Nature, Sky")
            time.sleep(1)
            art_is_mature.click()
            time.sleep(1)
            art_rights.click()
            time.sleep(10)
            save_button.click()
            time.sleep(50)

site_urls = ['https://www.redbubble.com/signup']
for url in site_urls:
    image_upload(url)

