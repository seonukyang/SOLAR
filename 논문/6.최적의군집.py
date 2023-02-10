import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
df = pd.read_csv('result_kmenas_논문_조정된3군집.csv', encoding = 'cp949')
list = ['area','capacity','realty_price','insolation','generation_quantity','economic_feasibility']
X = df[list]

inertia = []

scaler = StandardScaler().fit(X)
X_stand = scaler.transform(X)

for k in range(1,11) : 
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit_predict(X_stand)
    inertia.append(kmeans.inertia_)

plt.plot(range(1,11),inertia, marker='o')
plt.grid()
plt.show()