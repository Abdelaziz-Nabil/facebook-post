


from time import sleep
import xlsxwriter
from selenium import webdriver
import time


usr = input('Enter Email Id:')
pwd = input('Enter Password:')
#events_search = input('Enter Link:')#F:\work
driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
driver.get('https://m.facebook.com/login')
print("Opened facebook")
sleep(1)


username_box = driver.find_element_by_id('m_login_email')
username_box.send_keys(usr)
print("Email Id entered")
sleep(1)


password_box = driver.find_element_by_id('m_login_password')
password_box.send_keys(pwd)
print("Password entered")


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
worksheet.write('D1','City')
worksheet.write('E1','Country')


index=1
for url in ma:
    #load_post
    driver.get(url)
    sleep(4)
    
    #react
    react = driver.find_element_by_class_name("_45m8")
    react.click()
    sleep(4)
    
    #load_reacts
    x=True
    while(x==True):
        try:
            load = driver.find_element_by_class_name("content")
            load.click()
            sleep(4)
            x=True
        except:
            x=False
    
    load_url =driver.find_elements_by_class_name('darkTouch')
    profile_links = list()
    for li in load_url:
        profile_links.append(li.get_attribute('href'))
    
    for link in profile_links:
        index=index+1
        #load_profile
        driver.get(link)
        link_p=link.replace('https://m.','https://www.')
        sleep(5)
        
        #name
        try:
            try:
                name_=driver.find_element_by_id('cover-name-root')
                name=name_.text
            except:
                name_=driver.find_element_by_xpath("//*[contains(@class,'_59k _2rgt _1j-f _2rgt')]")
                name=name_.text
        except:
            name=''

        #id
        try:
            id = driver.find_elements_by_xpath("//*[contains(@class,'_4g34 _195r')]")
            id_text=(id[0].get_attribute('data-store'))
            try:
                p_id=((id_text.replace(',"profile_high_quality_metric":',':{"profile_id":')).split(':{"profile_id":'))[1]
            except:
                p_id=((id_text.replace(',"source":',':{"page_id":')).split(':{"page_id":'))[1]
        except:
            p_id=''
        
        
        #click_about
        try:
            about = driver.find_element_by_xpath("//*[contains(@class,'_5s61 _5cn0 _5i2i _52we')]")
            about.click()
            sleep(4)
        except:
            pass
        
        sleep(5)
        #Current town/city'
        try:
            address_ = driver.find_element_by_xpath("//*[contains(@class,'_4g34 _5b6q _5b6p _5i2i _52we')]")
            address=(((str(address_.text)).replace('\nHome town','')).replace('\nCurrent town/city','')).split(', ')
            if len(address)>2:
                city=address[0] + ', '+address[1]
                country=address[-1]
            else:
                city=address[0]
                country=address[-1] 
        except:
            city=''
            country=''
        
        #excel
        worksheet.write('A'+str(index),name)
        worksheet.write('B'+str(index),p_id)
        worksheet.write('C'+str(index),link_p)
        worksheet.write('D'+str(index),city)
        worksheet.write('E'+str(index),country)
        print('---------------'+str(index-1)+'---------------')
workbook.close()
print("Done")
input('Press anything to quit : ')
driver.quit()
print("Finished")

