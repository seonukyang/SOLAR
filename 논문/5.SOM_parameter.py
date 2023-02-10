from cProfile import label
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.decomposition import PCA
from minisom import MiniSom 



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


#표준화
X = df[list]
scaler = StandardScaler().fit(X)
X_stand = scaler.transform(X)


#결과를 답기 위해 컬럼 추가
df['result'] = ''

#SOM
#원하는 파라미터 조합 리스트화
map_n= [n for n in range(2,6)]
para_sigma= [np.round(sigma*0.1,2) for sigma in range(1,10)]
para_learning_rate= [np.round(learning_rate*0.1,2) for learning_rate in range(1,10)]

#결과 값을 담을 리스트 res 생성
res = []

for n in map_n:
    for sigma in para_sigma:
        for lr in para_learning_rate:  
            try:
                #랜덤으로 초기값을 설정하는 경우
                estimator = MiniSom(n,n,6,sigma =sigma, learning_rate = lr, topology='hexagonal', random_seed=0)
                estimator.random_weights_init(X_stand)
                estimator.train(X_stand,1000,random_order=True)
                qe = estimator.quantization_error(X_stand)
                #te = estimator.topographic_error(data.values)
                winner_coordinates = np.array([estimator.winner(x) for x in X_stand]).T
                cluster_index = np.ravel_multi_index(winner_coordinates,(n,n))
                
                res.append([str(n)+'x'+str(n),sigma,lr,'random_init',qe,len(np.unique(cluster_index))])

                #pca로 초기값을 설정하는 경우
                estimator = MiniSom(n,n,6,sigma =sigma, learning_rate = lr,topology='hexagonal', random_seed=0)
                estimator.pca_weights_init(X_stand)
                estimator.train(X_stand,1000,random_order=True)
                qe = estimator.quantization_error(X_stand)
                #te = estimator.topographic_error(data.values)
                winner_coordinates = np.array([estimator.winner(x) for x in X_stand]).T
                cluster_index = np.ravel_multi_index(winner_coordinates,(n,n))
                
                res.append([str(n)+'x'+str(n),sigma,lr,'pca_init',qe,len(np.unique(cluster_index))])
                
            except ValueError as e:
                print(e)
            
#결과 데이터프레임 생성 및 sorting 
df_res = pd.DataFrame(res,columns=['map_size','sigma','learning_rate','init_method','qe','n_cluster']) 
df_res.shape
df_res.sort_values(by=['qe'],ascending=True,inplace=True,ignore_index=True)
df_res.to_csv('SOM_best_parameter.csv', encoding = 'cp949', index=False)