import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sns

df = pd.read_csv('result_kmenas_논문_조정된3군집.csv', encoding = 'cp949')
list = ['area','capacity','realty_price','insolation','generation_quantity','economic_feasibility']
X = df[list]

inertia = []

scaler = StandardScaler().fit(X)
X_stand = scaler.transform(X)

# fig, axs = plt.subplots(1,6, figsize = (20,5))

# for column in list:
#     for i in range(0,len(list),1):
#         if list[i]==column :
#             sns.boxplot(X[column], ax = axs[i])
# plt.show()


for k in range(1,11) : 
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit_predict(X_stand)
    inertia.append(kmeans.inertia_)

plt.plot(range(1,11),inertia, marker='o')
plt.grid()
plt.show()