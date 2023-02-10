import pandas as pd
import numpy as np
import urllib.request
#selenium 이라는 다른 크롤링 라이브러리를 사용합니다.
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


data = {'id':[],'link':[]} 
df = pd.DataFrame(data)

id = int(0)
base_link = 'https://icomarks.com'


list_url = 'https://icomarks.com/icos?status=ended&sort=ending-desc&whitelist=&kyc=&bounty=&mvp=&email_confirmed='
sleep_time = 2
    
#chromedriver라는 python외의 별도의 응용프로그램을 사용합니다. 아래는 chromedriver를 작동시켜 원하는 url의 홈페이지를 여는 코드립니다.
#open webdriver
chrome_driver = 'C:\selenium\chromedriver'
driver = webdriver.Chrome(chrome_driver)
driver.get(list_url)

for i in range(0,40,1) : 
    xpath = '//*[@id="list"]/div[2]/div[2]/div[1]/div['+str(i+1)+']/div[2]'
    defence = driver.find_element_by_xpath(xpath)
    tags = defence.get_attribute('innerHTML')
    url = tags[37:].split('\">')[0]
    real_url = base_link+url
    newdata = {'id':id, 'link': real_url}
    df = df.append(newdata, ignore_index=True) 
    id = id+1


driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

#홈페이지가 스크롤을 아래로 내려야 새로운 목록이 갱신되는 동적 홈페이지 입니다. 스크롤을 내리기 위한 시간을 벌기 위해 3초의 유예시간을 주었습니다.
time.sleep(3)

#홈페이지 리스트가 40번째 부터는 양식이 달라지기 때문에 다른 for문을 사용하였습니다.
for i in range(40,281,1) : 
    time.sleep(1)
    for j in range(0,20,1) : 
        xpath = '//*[@id="list"]/div[2]/div[2]/div[1]/div['+str(i+1)+']/div['+str(j+1)+']/div[2]'
        defence = driver.find_element_by_xpath(xpath)
        tags = defence.get_attribute('innerHTML')
        url = tags[37:].split('\">')[0]
        real_url = base_link+url
        newdata = {'id':id, 'link': real_url}
        df = df.append(newdata, ignore_index=True) 
        id = id+1

#홈페이지 리스트의 마지막은 목록의 수량이 부족하기 때문에 별도의 for문을 작성하였습니다.
for j in range(0,11,1) : 
    time.sleep(1)
    xpath = '//*[@id="list"]/div[2]/div[2]/div[1]/div[282]/div['+str(j+1)+']/div[2]'
    defence = driver.find_element_by_xpath(xpath)
    tags = defence.get_attribute('innerHTML')
    url = tags[37:].split('\">')[0]
    real_url = base_link+url
    newdata = {'id':id, 'link': real_url}
    df = df.append(newdata, ignore_index=True) 
    id = id+1


driver.close()
driver.quit()

df.to_csv('search_link2.csv', encoding='utf-8-sig')