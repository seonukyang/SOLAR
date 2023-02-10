import pandas as pd

df_kmeans2 = pd.read_csv('result_kmeans_논문_2_이상값제거.csv', encoding = 'cp949')
df_kmeans3 = pd.read_csv('result_kmeans_논문_3_이상값제거.csv', encoding = 'cp949')
df_kmeans4 = pd.read_csv('result_kmeans_논문_4_이상값제거.csv', encoding = 'cp949')
df_dbscan = pd.read_csv('result_dbscan_논문_이상값제거.csv', encoding = 'cp949')
df_som = pd.read_csv('result_som_논문_이상값제거.csv', encoding = 'cp949')

df = df_kmeans2[['id','proprietary_institution','line','area','유형분류','현재 사용현황','향후 사용계획 및 추진사항','plan_category',
'capacity','land_category','realty_price','sys_connection','sys_connection','sys_connection','sys_connection']]
df['cluster_kmeans2'] = df_kmeans2['result']
df['cluster_kmeans3'] = df_kmeans3['result']
df['cluster_kmeans4'] = df_kmeans4['result']
df['cluster_dbscan'] = df_dbscan['result']
df['cluster_som'] = df_som['result']
print(df)

group_kmeans2_kmeans3 = df.groupby(['cluster_kmeans2','cluster_kmeans3'])
print(group_kmeans2_kmeans3.size())

group_kmeans2_dbscan = df.groupby(['cluster_kmeans2','cluster_dbscan'])
print(group_kmeans2_dbscan.size())

group_kmeans3_dbscan = df.groupby(['cluster_kmeans3','cluster_dbscan'])
print(group_kmeans3_dbscan.size())

group_som_kmeans2 = df.groupby(['cluster_som','cluster_kmeans2'])
print(group_som_kmeans2.size())

group_som_kmeans3 = df.groupby(['cluster_som','cluster_kmeans3'])
print(group_som_kmeans3.size())

group_som_dbscan = df.groupby(['cluster_som','cluster_dbscan'])
print(group_som_dbscan.size())

group_som_kemans2_dbscan = df.groupby(['cluster_som','cluster_kmeans2','cluster_dbscan','plan_category'])
print(group_som_kemans2_dbscan.size())

group_som_kemans3_dbscan = df.groupby(['cluster_som','cluster_kmeans3','cluster_dbscan','plan_category'])
print(group_som_kemans3_dbscan.size())

print(df['cluster_som'].value_counts())