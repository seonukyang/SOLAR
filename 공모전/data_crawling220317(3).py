import pandas as pd
import numpy as np
import urllib.request
from bs4 import BeautifulSoup as bs
import re
from selenium import webdriver
from pandas.io.html import read_html
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

dict = {'year':[],'volumn':[],'season':[],'table':[],'keyword':[],'url':[] }
df = pd.DataFrame(dict) 

for volume in range(46,47,1) : 
# for volume in range(1,2,1) :
    print('volume = ', volume)
    for season in range(1,2,1) : 
        if volume < 10 : 
            volume_text = '0'+str(volume)
        else : volume_text = volume

        url_base = 'https://misq.umn.edu/contents-'+str(volume_text)+'-'+str(season)
        req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        soup = bs(html, 'html.parser')

        tags = soup.select('#maincontent > div.columns > div')
        table_list =  str(tags).replace('\n','').split('<p style="padding-left: 1em;"><a href=')

        for table_num in range(1, len(table_list),1) :     
            url_target = table_list[table_num].split('"')[1]         
            print(url_target) 
            driver = webdriver.Chrome('./chromedriver')
            driver.get(url_target)
            text_list = driver.find_elements_by_xpath('//*[@id="maincontent"]/div[2]/div/div[4]/div[2]/div/table/tbody/tr[5]/td[2]')
            print(text_list)
            keyword = text_list[0].text

            newdata = {'year':int(volume)+1976,'volumn':volume,'season':season,'table':table_num,'keyword':keyword,'url':url_target }
            df =  df.append(newdata, ignore_index=True)
df.to_excel('raw data_220319_add.xlsx', encoding='utf-8-sig', index = None, header=True)

            