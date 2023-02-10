from cProfile import label
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.decomposition import PCA

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

print(df.shape)

#박스그림
X = df[list]
fig, axs = plt.subplots(1,6, figsize = (20,5))

for column in list:
    for i in range(0,len(list),1):
        if list[i]==column :
            sns.boxplot(X[column], ax = axs[i])
# plt.show()
plt.clf()

#표준화
scaler = StandardScaler().fit(X)
X_stand = scaler.transform(X)

#eldow method
inertia = []
for k in range(1,11) : 
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit_predict(X_stand)
    inertia.append(kmeans.inertia_)
    # print(k,'번째 inertia : ',inertia[k-1])
    # if k > 1 : 
        # print(k-1,' -> ',k,' inertia의 감소량 : ',inertia[k-2]-inertia[k-1])

plt.plot(range(1,11),inertia, marker='o')
plt.grid()
# plt.show()
plt.clf()



#결과를 답기 위해 컬럼 추가
df['result'] = ''

#군집화 분석
kmeans = KMeans(n_clusters=3, random_state=0)
Y_kmeans = kmeans.fit_predict(X_stand)
S_score = silhouette_score(X_stand, Y_kmeans)
C_score = calinski_harabasz_score(X_stand, Y_kmeans)
print('실루엣 계수:',S_score)
print('CH계수: ',C_score)
print(df.shape)

for i in range(0,len(df),1):
    df['result'].iloc[i] = Y_kmeans[i]

result_group = df.groupby(['plan_category','result'])
print(result_group.size())

#2차원으로 군집 시각화
pca = PCA(n_components=2)
pca_transformed = pca.fit_transform(X_stand)

df['pca_x'] = pca_transformed[:,0]
df['pca_y'] = pca_transformed[:,1]
center = kmeans.cluster_centers_

markers = ['o','s','^','P','D','H','x']
colors = ['r','b','g','violet']
plt.figure(figsize=(14,8))
for i in range(0,3,1):
# cluster 값이 0, 1, 2 인 경우마다 별도의 Index로 추출
    marker_ind = df[df['result']==i].index

    # cluster값 0, 1, 2에 해당하는 Index로 각 cluster 레벨의 pca_x, pca_y 값 추출. o, s, ^ 로 marker 표시
    plt.scatter(x=df.loc[marker_ind,'pca_x'], y=df.loc[marker_ind,'pca_y'], c=colors[i], 
    marker=markers[i], label='cluster '+str(i)) 
    pca_center = pca.fit_transform(center)

    plt.scatter(x=pca_center[i,0], y=pca_center[i,1], s=200, color='white', alpha=0.9, edgecolor='k', marker='o')
    plt.scatter(x=pca_center[i,0], y=pca_center[i,1], s=60, color='k',edgecolor='k', marker='$%d$' % i)

#그림 상세 설정
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.legend(loc='upper right')
plt.title('3 Clusters Visualization by 2 PCA Components')
plt.show()

df.to_csv('result_kmeans_논문_3_이상값제거.csv', encoding = 'cp949', index=False)

#spss용 데이터
df_spss = df[['area','capacity','realty_price','insolation','generation_quantity','economic_feasibility','result']]
# df_spss.to_csv('SPSS_kmeans_논문_3_이상값제거_utf.csv', encoding = 'utf-8', index=False)


#사후분석 통계값
result_group = df.groupby(['result'])
result_group_analysis = result_group.aggregate(['mean','std'])
print(result_group.aggregate(['mean','std']))

# result_group_analysis.to_csv('after_analysis_논문_3군집_이상값제거.csv', encoding = 'cp949', index=False)

result_total_analysis = df.aggregate(['mean','std'])
# result_total_analysis.to_csv('after_analysis_total_논문_3군집_이상값제거.csv', encoding = 'cp949', index=False)