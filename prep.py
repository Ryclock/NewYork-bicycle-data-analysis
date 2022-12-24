import gc
import time

import pandas as pd
from pympler import tracker

from process import *


# 批量处理数据
def batch(dateList: list, year_info: str) -> None:
    print(year_info+' started at {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
    # 数据预处理
    for date in dateList:
        # 清洗
        df = utils.load('data/original/'+date+'-citibike-tripdata.csv')
        utils.drop_abnormal(data=df, savepath='data/clear/'+date+'.csv')
        print(date+' finish clear')
        del df
        time.sleep(1)
    # 站点信息表提取（以第一个月为准，不考虑新增站点和移除站点）
    df = utils.load('data/clear/'+dateList[0]+'.csv')
    filter.get_stationInfo_csv(
        data=df, savepath='data/siteInfo/'+year_info+'.csv')
    print(year_info+' finish siteInfo')
    # 流量信息表提取
    for date in dateList:
        df = utils.load('data/clear/'+date+'.csv')
        filter.get_trafficInfo_csv(
            data=df, savepath='data/trafficInfo/'+date+'.csv')
        print(date+' finish trafficInfo')
        del df
        time.sleep(1)
    # 时空聚类
    # 聚类信息获取（以第一个月为准，不考虑新增站点和移除站点）
    cluster_ST.cluster_Kmeans(n=100, filepath='data/siteInfo/'+year_info+'.csv',
                              savepath='data/clusterInfo/'+year_info+'.csv')
    print(year_info+' finish clusterInfo')
    # 簇间/内流量信息获取
    for date in dateList:
        cluster_ST.aggregate_interclass(StoC_filepath='data/siteInfo/'+year_info+'.csv',
                                        folderpath='data/trafficInfo/detail/'+date,
                                        savepath='data/cluster_ST/'+date+'.json')
        print(date+' finish cluster_ST')
        time.sleep(2)
    # 时域聚类
    matrix = pd.DataFrame(columns=['rub'])
    # 每月流量矩阵获取
    for date in dateList:
        feature = cluster_T.matrix_month(
            n=100, folderpath='data/trafficInfo/detail/' + date)
        matrix = pd.concat([matrix, feature], axis=0)
        print(date+' get cluster_T features')
        del feature
    matrix = matrix.drop(columns=['rub'])
    # 聚类结果生成（以年为集合）
    cluster_T.cluster_Kmeans(n=4, features=matrix,
                             savepath='data/cluster_T/'+year_info+'.csv')
    del matrix
    gc.collect()
    time.sleep(20)
    print(year_info+' finished All at {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))


# 示例
def demo(year: str) -> None:
    dateList = []
    for date in pd.date_range(start=year+'0101', periods=12, freq='M'):
        dateList.append(pd.to_datetime(date).strftime('%Y%m'))
    batch(dateList, year)


if __name__ == '__main__':
    tr = tracker.SummaryTracker()
    tr.print_diff()
    print('process started at {}'.format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
    demo('2019')
    demo('2020')
    print('process finished at {}'.format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
    tr.print_diff()
