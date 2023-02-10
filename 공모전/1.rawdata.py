import numpy as np
import pandas as pd

df = pd.read_csv('국가철도공단_철도유휴부지DB_20210902.csv', encoding = 'cp949')
plan_list = ['없음','계획 없음','활용계획 검토 중','계속 사용허가(태양광)','사용허가(태양광)','태양광부지 사용허가']
rawdata_df = df[df['향후 사용계획 및 추진사항']==plan_list[0]]

for plan in plan_list[1:] : 
    rawdata_df_new = df[df['향후 사용계획 및 추진사항']==plan]
    rawdata_df = pd.concat([rawdata_df, rawdata_df_new], axis = 0)

rawdata_df.to_csv('rawdata.csv',encoding='cp949')