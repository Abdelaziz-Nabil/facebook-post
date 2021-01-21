#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from time import sleep
import xlsxwriter
from selenium import webdriver
import numpy as np
import random
import time


delays = [7, 10, 6,9,5,8]

usr = input('Enter Email Id:')
pwd = input('Enter Password:')
driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
driver.get('https://m.facebook.com/login')
print("Opened facebook")
sleep(4)


username_box = driver.find_element_by_id('m_login_email')
username_box.send_keys(usr)
print("Email Id entered")
sleep(3)


password_box = driver.find_element_by_id('m_login_password')
password_box.send_keys(pwd)
print("Password entered")
sleep(3)

login_box = driver.find_element_by_name('login')
login_box.click()
sleep(4)


f = open("URL.txt", "r")
ma=list()
for x in f:
    ma.append((x.replace('https://www.','https://m.')).replace('\n',''))
    print(ma[-1])
    
    

fileexcel=open("DATA.xlsx",'a')
workbook = xlsxwriter.Workbook("DATA.xlsx")
worksheet=workbook.add_worksheet()
worksheet.write('A1','Name')
worksheet.write('B1','ID')
worksheet.write('C1','URL')
index=1
for url in ma:
    #load_post
    driver.get(url)
    delay = np.random.choice(delays)
    sleep(delay)
    
    #react
    react = driver.find_element_by_class_name("_45m8")
    react.click()
    sleep(4)
    number =0
    #load_reacts
    x=True
    while(x==1):
        try:
            number =number+1
            print(number)
            sleep(delay)
            load = driver.find_element_by_class_name("content")
            load.click()
            sleep(delay)
            x= int (input('Enter x:'))
        except:
            x=0
    
    
    user_info =  driver.find_elements_by_xpath("//*[contains(@class,'ib cc _1aj4')]")
    link_list=list()
    name_d={}
    for li in user_info:
        index=index+1
        user_link=(li).find_element_by_class_name('darkTouch')
        link=user_link.get_attribute('href')
        name=li.text
        name=name.replace('\nFollow','')
        link=link.replace('https://m.','https://www.')
        name_d[link] = name
        link_list.append(link)
        id=((((link.replace('https://www.facebook.com/profile.php?id=','')).replace('/?fref=pb','')).replace('?fref=pb','')).replace('https://www.facebook.com/','')).replace('&fref=pb','')
        worksheet.write('A'+str(index),name)
        worksheet.write('B'+str(index),id)
        worksheet.write('C'+str(index),link)

    sleep(20)
        
        
workbook.close()
print("Done")
input('Press anything to quit : ')
driver.quit()
print("Finished")

