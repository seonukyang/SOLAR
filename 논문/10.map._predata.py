import pandas as pd
import numpy as np

df = pd.read_csv('주소.csv', encoding = 'cp949')
data_all = df.transpose().index

latitude = []
longtitude = []

for data in data_all : 
    data_latitude = str(data.replace('(','').split(')')[0].split(', ')[0])
    latitude.append(data_latitude)
    data_longtitude = str(data.replace('(','').split(')')[0].split(', ')[1])
    longtitude.append(data_longtitude)

data_dict = {'latitude': latitude, 'longitude': longtitude}
result = pd.DataFrame(data_dict)

result.to_csv('SOM_group2_coordinate.csv', encoding = 'cp949', index=False)
