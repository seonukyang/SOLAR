from cmath import nan
import pandas as pd
import numpy as np
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#크롤링이 중단된 번호를 입력하여 다시 진행
num = 1213

df = pd.read_csv('데이터모음/traindata_논문_'+str(num)+'.csv', encoding = 'cp949')

def data_crawling(i) : 
 #chromedrive 기동 
    url_target = 'https://recloud.energy.or.kr/service/regi_require.do' 
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url_target)
    driver.implicitly_wait(time_to_wait=5)

    #1페이지 주소 입력 단계
    address_list = (df['address'][i]).split(' ')
    driver.find_element(By.XPATH,"//*[@id=\"addr_click2\"]").click()
    # sleep(3)

    #시도 입력 - 드랍박스
    # sleep(0.5)
    sido = Select(driver.find_element(By.ID,'sido'))
    sido.select_by_visible_text(str(address_list[0]))

    #시군구 입력 - 드랍박스
    # sleep(0.5)
    if str(address_list[1]) == '여주군' : 
        address_list[1] = '여주시'
    if str(address_list[2])[-1] == '구' : 
        gugun = Select(driver.find_element(By.ID,'gugun'))
        gugun.select_by_visible_text(str(address_list[1])+' '+str(address_list[2])) 
    else:
        gugun = Select(driver.find_element(By.ID,'gugun'))
        gugun.select_by_visible_text(str(address_list[1]))

    #읍면동 입력 - 드랍박스
    #sleep(0.5)
    if str(address_list[2]) == '홍북면' : 
        address_list[2] = '홍북읍'
    if str(address_list[2]) == '실촌읍' : 
        address_list[2] = '곤지암읍'

    if str(address_list[2])[-1] == '구' : 
        dong = Select(driver.find_element(By.ID,'dong'))
        dong.select_by_visible_text(str(address_list[3]))
    else : 
        dong = Select(driver.find_element(By.ID,'dong'))
        dong.select_by_visible_text(str(address_list[2]))

    #리+산의 경우
    if str(address_list[2])[-1] == '구' : 
        if len(address_list)==7:
            #sleep(0.5)
            li = Select(driver.find_element(By.ID,'li'))
            li.select_by_visible_text(str(address_list[4]))
                    
            #sleep(0.5)
            addr_land = Select(driver.find_element(By.ID,'addr_land'))
            addr_land.select_by_visible_text(str(address_list[5]))
        elif address_list[4][-1]=='리':
            #sleep(0.5)
            li = Select(driver.find_element(By.ID,'li'))
            li.select_by_visible_text(str(address_list[4]))
        elif address_list[4][-1]=='산':
            #sleep(0.5)
            addr_land = Select(driver.find_element(By.ID,'addr_land'))
            addr_land.select_by_visible_text(str(address_list[4]))
        
    else :
        if len(address_list)==6:
            #sleep(0.5)
            li = Select(driver.find_element(By.ID,'li'))
            li.select_by_visible_text(str(address_list[3]))
                        
            #sleep(0.5)
            addr_land = Select(driver.find_element(By.ID,'addr_land'))
            addr_land.select_by_visible_text(str(address_list[4]))

    #리의 경우
        elif address_list[3][-1]=='리':
            #sleep(0.5)
            li = Select(driver.find_element(By.ID,'li'))
            li.select_by_visible_text(str(address_list[3]))

    #산의 경우
        elif address_list[3][-1]=='산':
            #sleep(0.5)
            addr_land = Select(driver.find_element(By.ID,'addr_land'))
            addr_land.select_by_visible_text(str(address_list[3]))
            
    #본번, 부번 입력
    #본번 부번 다 있는 경우
    if len(address_list[-1].split('-'))>1:
        #sleep(0.5)
        driver.find_element(By.ID,'addr_bobn').send_keys(address_list[-1].split('-')[0])
        #sleep(0.5)
        driver.find_element(By.ID,'addr_bubn').send_keys(address_list[-1].split('-')[1])
    #부번이 없는 경우
    else : 
        #sleep(0.5)
        driver.find_element(By.ID,'addr_bobn').send_keys(address_list[-1])
        #sleep(0.5)
        driver.find_element(By.ID,'addr_bubn').send_keys('0')

    #설치용량 입력 및 저장
    capacity = int(df['area'][i]/13)
    df['capacity'].iloc[i] = capacity
    #sleep(1)
    driver.find_element(By.XPATH,'//*[@id="install_capacity"]').send_keys(capacity)
            
    #상세분석 입력
    #sleep(0.5)
    driver.find_element(By.XPATH,'//*[@id="sub-container"]/div/div/form/fieldset/div[2]/input').click()

    #1단계 페이지 진입
    #팝업 클릭
    #sleep(3)
    driver.find_element(By.XPATH,'/html/body/div[15]/div[1]/div/div[2]/a').click()
            
    #지목 저장
    #sleep(4)
    df['land_category'].iloc[i] = driver.find_element(By.XPATH,'//*[@id="property_list2"]/tbody/tr[1]/td').text

    #공시지가 저장
    driver.execute_script('window.scrollTo(0, 800);')
    sleep(4)
    realty_price = driver.find_element(By.XPATH,'//*[@id="property_list2"]/tbody/tr[8]/td')
    if realty_price.text =='' :
        #sleep(1)
        driver.close()
        
    else :
        realty_price = realty_price.text.split(' ')[0]
        if realty_price == 'Money-XXX':
            df['realty_price'].iloc[i] = ''
            #sleep(1)
            driver.close()
        else : 
            df['realty_price'].iloc[i]= int(realty_price.replace(',',''))     
                
            #2단계 버튼 클릭
            #sleep(1)
            driver.find_element(By.XPATH,'//*[@id="sub-container"]/div/div/fieldset/div/div[2]/ol/li[2]/a').click()

            #2단계 페이지 진입
            #계통연계 조사
            #sleep(4)
            sys_connection = ''
            j=1
            df['sys_connection'].iloc[i]='불가능'
            while(j<10):
                try : 
                    sys_connection = driver.find_element(By.XPATH,'//*[@id="table"]/tr['+str(j)+']/td[3]')
                    if int(sys_connection.text.replace(',','')) > df['capacity'].iloc[i] : 
                        df['sys_connection'].iloc[i]='가능'
                        break
                    j+=1
                except : 
                    break

            #3단계 버튼 클릭
            #sleep(1)
            driver.find_element(By.XPATH,'//*[@id="sub-container"]/div/div/fieldset/div/div[2]/ol/li[3]/a').click() 

            #3단계 페이지 진입
            #sleep(4)
            driver.find_element(By.XPATH,'//*[@id="tb_list_12"]').click() 
            #sleep(2)
            insolation = 0.00
            for m in range(2,14,1):
                insolation = insolation + float(driver.find_element(By.XPATH,'//*[@id="tb_view_12"]/div/table/tbody/tr[1]/td['+str(m)+']').text)
            df['insolation'].iloc[i] = round(insolation/12,2)

            #4단계 버튼 클릭
            #sleep(1)
            driver.find_element(By.XPATH,'//*[@id="sub-container"]/div/div/fieldset/div/div[2]/ol/li[4]/a').click() 

            #4단계 페이지 진입
            #sleep(4)
            df['generation_quantity'].iloc[i] = int(driver.find_element(By.XPATH,
            '//*[@id="sub-container"]/div/div/fieldset/div/div[4]/div[1]/div/dl/dd/span').text.replace(',',''))

            #5단계 버튼 클릭
            #sleep(1)
            driver.find_element(By.XPATH,'//*[@id="sub-container"]/div/div/fieldset/div/div[2]/ol/li[5]/a').click() 

            #5단계 페이지 진입
            #경제성
            #SMP, REC방식을 소형태양광 고정가격계약 매입으로 변경
            #sleep(4)
            if capacity < 30:
                driver.find_element(By.XPATH,'//*[@id="info_tab4"]/a').click()
            else : driver.find_element(By.XPATH,'//*[@id="info_tab2"]/a').click()
            sleep(2)
            df['economic_feasibility'].iloc[i] = int(driver.find_element(By.XPATH,'//*[@id="result_avg3"]').text.replace(',',''))

            #sleep(1)
            driver.close()


# for i in range(251,258,1) : 
for i in range(0,375,1) :  
    df['address'].iloc[i] = df['address'].iloc[i].replace('ㅡ','-')
    if int(df['area'][i]/13) > 0 :
        try : 
            data_crawling(i)
        except :
            data_crawling(i)
            
df.to_csv('데이터모음/traindata_논문_추가'+str(num)+'.csv', encoding = 'cp949', index=False)