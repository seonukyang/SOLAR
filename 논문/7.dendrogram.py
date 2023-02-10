from cProfile import label
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
import numpy as np

df = pd.read_csv('traindata_논문_2520.csv', encoding = 'cp949')

#결측치 삭제 - 지목이 없는 데이터 삭제
df = df.dropna()

#계통 연계가 불가능인 데이터 삭제
df = df.drop(df[df['sys_connection'] == '불가능'].index)

#설치용량이 0인 데이터 삭제
df = df.drop(df[df['capacity'] ==  0].index)


#박스그림
list = ['area','capacity','realty_price','insolation','generation_quantity','economic_feasibility']


#IQR지정
for a in list : 
    Q1 = df[a].quantile(0.25)
    Q3 = df[a].quantile(0.75)
    IQR = Q3 - Q1

    lower_outlier_index = df[(df[a] < Q1 - 2*IQR)].index
    uper_outlier_index = df[(df[a]) > Q3 + 2*IQR].index
    df.drop(lower_outlier_index, inplace = True)
    df.drop(uper_outlier_index, inplace = True)


X = df[list]

#표준화
scaler = StandardScaler().fit(X)
X_stand = scaler.transform(X)

# methods = ['ward','centroid', 'median']
methods = ['ward']
for method in methods : 
    h_cluster = linkage(X_stand, method = method)
    
    plt.figure(figsize = (10,10))
    plt.title('Ward Method\'s Dendrogram')
    plt.xlabel('Railway Unused Land')
    plt.ylabel('Distance')
    plt.xticks([0,1000])
    dendrogram(h_cluster)
    plt.show()
    
