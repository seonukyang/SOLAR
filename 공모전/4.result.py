import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.cluster import KMeans

df = pd.read_csv('traindata_final.csv', encoding = 'cp949')
list = ['area','capacity','realty_price','insolation','generation_quantity','economic_feasibility']
X = df[list]

#결과를 답기 위해 컬럼 추가
df['result'] = ''

#표준화
scaler = StandardScaler().fit(X)
X_stand = scaler.transform(X)

#군집화 분석
kmeans = KMeans(n_clusters=3, random_state=0)
Y_kmeans = kmeans.fit_predict(X_stand)
S_score = silhouette_score(X_stand, Y_kmeans)
C_score = calinski_harabasz_score(X_stand, Y_kmeans)
print(S_score, C_score)

for i in range(0,len(df),1):
    df['result'].iloc[i] = Y_kmeans[i]

df.to_csv('result_kmenas_3.csv', encoding = 'cp949', index=False)