import numpy as np
import pandas as pd



df = pd.read_csv('국가철도공단_철도유휴부지DB_20210902_논문.csv', encoding = 'cp949')
plan_list = ['-','미사용','없음','계획 없음','활용계획 검토 중','계속 사용허가(태양광)','사용허가(태양광)','태양광부지 사용허가','태양광발전사업']
rawdata_df = df[df['향후 사용계획 및 추진사항']==plan_list[0]]

def plan_category(plan):
    switcher = {
        '-': "계획없음",
        '미사용':'계획없음',
        '없음' : '계획없음',
        '계획 없음' : '계획없음',
        '활용계획 검토 중' : '계획없음',
        '계속 사용허가(태양광)' : '태양광사용',
        '사용허가(태양광)' : '태양광사용',
        '태양광부지 사용허가' : '태양광사용',
        '태양광발전사업' : '태양광사용'
    }
    return switcher.get(plan, "nothing")

for plan in plan_list[1:] : 
    rawdata_df_new = df[df['향후 사용계획 및 추진사항']==plan]
    rawdata_df = pd.concat([rawdata_df, rawdata_df_new], axis = 0)

rawdata_df['plan_category'] = ''
for i in range(0,len(rawdata_df),1) : 
    rawdata_df['plan_category'].iloc[i] = plan_category(rawdata_df['향후 사용계획 및 추진사항'].iloc[i])


rawdata_df.to_csv('rawdata_논문.csv',encoding='cp949')