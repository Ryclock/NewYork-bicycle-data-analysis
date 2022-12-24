import json
import os
from multiprocessing import Pool
from typing import Union

import pandas as pd
from sklearn.cluster import KMeans


# 获取Kmeans聚类结果表
def cluster_Kmeans(n: int, filepath: str, savepath: str) -> None:
    sInfo = pd.read_csv(filepath)
    est = KMeans(n_clusters=n, tol=0).fit(sInfo[['sLongitude', 'sLatitude']])
    sInfo['clusterID'] = est.predict(sInfo[['sLongitude', 'sLatitude']])
    cInfo = pd.DataFrame(data={
        'cLongitude': list(map(lambda x: x[0], est.cluster_centers_)),
        'cLatitude': list(map(lambda x: x[1], est.cluster_centers_)),
        'stationID': [sInfo.query('clusterID==@cID')['sID'].tolist() for cID in range(n)]
    })
    del est
    sInfo.to_csv(filepath, index=False)
    del sInfo
    cInfo.index.name = 'clusterID'
    dirname = os.path.dirname(savepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    cInfo.to_csv(savepath)


# 获取详细的聚类间流量信息
def aggregate_interclass(StoC_filepath: str, folderpath: str, savepath: str) -> None:
    sInfo = pd.read_csv(StoC_filepath)
    if not folderpath.endswith('/'):
        folderpath += '/'
    result_list = []
    p = Pool(processes=os.cpu_count()//4)
    for day in range(1, 32):
        res = p.apply_async(subtask, (day, sInfo, folderpath))
        result_list.append(res)
    p.close()
    p.join()
    del sInfo
    dict = {}
    for res in result_list:
        date, records = res.get()
        dict[date] = records
    dirname = os.path.dirname(savepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    with open(savepath, 'w')as fp:
        json.dump(dict, fp)


# 子任务
def subtask(day: int, sInfo: pd.DataFrame, folderpath: str) -> Union[str, list]:
    try:
        date = None
        records = []
        detail = pd.read_csv(
            filepath_or_buffer=folderpath+str(day)+'.csv',
            dtype={
                'startDate': str,
                'sID_start': int,
                'sID_end': int,
                'count': int,
            })
        date = detail.loc[0, 'startDate']
        for index, value in detail['sID_start'].items():
            res = sInfo.query('sID==@value')
            if not res.empty:
                detail.loc[index, 'cID_start'] = res['clusterID'].values[0]
        for index, value in detail['sID_end'].items():
            res = sInfo.query('sID==@value')
            if not res.empty:
                detail.loc[index, 'cID_end'] = res['clusterID'].values[0]
        detail = detail.dropna(axis=0, how='any', inplace=False).astype(
            {'cID_start': 'int32', 'cID_end': 'int32'})  # 防止这两行数据类型被篡改
        detail.to_csv(folderpath+str(day)+'.csv', index=False)  # 更新每天的流量信息表
        detail = detail.rename(
            columns={'sID_start': 'from', 'sID_end': 'to'})
        inter = detail.drop(columns=['startDate', 'from', 'to'])
        sum = inter.groupby(
            by=['cID_start', 'cID_end']).sum().reset_index()
        del inter
        for index, row in sum.iterrows():
            sub = {}
            sub['from'] = int(row['cID_start'])
            sub['to'] = int(row['cID_end'])
            sub['count'] = int(row['count'])
            start = row['cID_start']
            end = row['cID_end']
            sub['detail_trip'] = detail.query(
                'cID_start==@start and cID_end==@end')[['from', 'to', 'count']].to_dict(orient='records')
            records.append(sub)
    except FileNotFoundError:
        print(folderpath+str(day) +
              '.csv Not Found, maybe this month don\'t have this day. ')
    except Exception as e:
        print(e)
    finally:
        print('subtask {} has finish'.format(date))
        return date, records
