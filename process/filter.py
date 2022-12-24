import os

import pandas as pd


# 获取站点信息表
def get_stationInfo_csv(data: pd.DataFrame, savepath: str) -> None:
    start = pd.DataFrame(data={
        'sID': data['start station id'],
        'sName': data['start station name'],
        'sLongitude': data['start station longitude'],
        'sLatitude': data['start station latitude'],
    })
    end = pd.DataFrame(data={
        'sID': data['end station id'],
        'sName': data['end station name'],
        'sLongitude': data['end station longitude'],
        'sLatitude': data['end station latitude'],
    })
    table = pd.concat([start, end]).drop_duplicates(subset='sID')
    del start, end
    dirname = os.path.dirname(savepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    table.to_csv(path_or_buf=savepath, index=False)


# 获取流量信息表
def get_trafficInfo_csv(data: pd.DataFrame, savepath: str) -> None:
    table = pd.DataFrame(data={
        'startDate': data['starttime'].dt.date,
        'sID_start': data['start station id'],
        'sID_end': data['end station id'],
    })
    table = pd.DataFrame(table.value_counts()).rename(
        columns={0: 'count'}).reset_index()
    dirname = os.path.dirname(savepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    table.to_csv(path_or_buf=savepath, index=False)
    # 细分每天的流量信息表
    basename = os.path.basename(savepath)
    for date in set(data['starttime'].dt.date):
        folder = dirname+'/detail/'+basename.split('.')[0]+'/'
        if not os.path.isdir(folder):
            os.makedirs(folder)
        subtable = table.query('startDate == @date')
        subtable.to_csv(
            path_or_buf=folder+str(date.day)+'.csv',
            index=False
        )
