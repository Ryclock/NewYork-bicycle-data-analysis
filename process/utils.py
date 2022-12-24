import os

import pandas as pd


# 导入数据
def load(filepath: str) -> pd.DataFrame:
    data = pd.read_csv(
        filepath_or_buffer=filepath,
        encoding='utf-8',
        dtype={
            'start station id': str,
            'end station id': str,
        },
        parse_dates=['starttime', 'stoptime'],
        infer_datetime_format=True,
    )
    return data


# 去除异常数据
def drop_abnormal(data: pd.DataFrame, savepath: str) -> None:
    # print(len(data))
    data = data.dropna(axis=0)
    data = data.query('tripduration >= 120 and tripduration <= 21600')
    # print(len(data))
    dirname = os.path.dirname(savepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    data.to_csv(path_or_buf=savepath, index=False)
