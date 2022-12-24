import os
from typing import Union

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


# 生成聚类流量的某一天对应的向量
def matrix_day(n: int, filepath: str) -> Union[str, pd.Series]:
    try:
        day = None
        vector = None
        detail = pd.read_csv(
            filepath_or_buffer=filepath,
            dtype={
                'startDate': str,
                'sID_start': int,
                'sID_end': int,
                'cID_start': int,
                'cID_end': int,
                'count': int,
            })
        startDataList = detail['startDate']
        matrix = pd.DataFrame(
            index=range(0, n),
            columns=range(0, n),
        )
        inter = detail.drop(columns=['startDate', 'sID_start', 'sID_end'])
        del detail
        sum = inter.groupby(
            by=['cID_start', 'cID_end']).sum().reset_index()
        del inter
        for index, row in sum.iterrows():
            matrix.loc[row['cID_start'], row['cID_end']] = row['count']
        day = startDataList[0]
        vector = matrix.unstack()
    except FileNotFoundError:
        print(filepath+'Not Found, maybe this month don\'t have this day. ')
    except Exception as e:
        print(e)
    finally:
        return day, vector


# 生成聚类流量的某一月对应的矩阵
def matrix_month(n: int, folderpath: str) -> pd.DataFrame:
    if not folderpath.endswith('/'):
        folderpath += '/'
    matrix = pd.DataFrame(
        index=pd.MultiIndex.from_product([range(0, n), range(0, n)]),
    )
    for i in range(1, 32):
        day, vector = matrix_day(n, folderpath+str(i)+'.csv')
        if day:
            matrix.insert(i-1, day, vector)
    index = []
    for i, j in matrix.index:
        index.append(str(i)+'-'+str(j))
    matrix.index = index
    return matrix.T


# 获取Kmeans聚类结果
def cluster_Kmeans(n: int, features: pd.DataFrame, savepath: str) -> pd.DataFrame:
    features = features.dropna(axis=0, how='all').fillna(0)
    est = KMeans(n_clusters=n).fit(features)
    idx = np.argsort(np.sum(a=est.cluster_centers_, axis=1))
    lut = np.zeros_like(idx)
    lut[idx] = np.arange(n)
    res = pd.DataFrame(
        columns=['label'],
        index=features.index,
        data=lut[est.labels_],
    )
    del est
    res.index.name = 'date'
    dirname = os.path.dirname(savepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    res.to_csv(savepath)
    return res
