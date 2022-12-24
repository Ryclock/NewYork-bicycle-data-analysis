from numbers import Number

import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Calendar
from pyecharts.commons.utils import JsCode

#!需要手动加入(202003数据部分)
# "calendarIndex":1,


# 归一化函数
def normalize(data: Number, max: Number, min: Number) -> float:
    return 1.0*(1-0)*(data-min)/(max-min) + 0


# 获取各群体每日使用单车次数，用于'usertype',一级检索为'Subscriber','Customer'
def count_times_usertype(dataset: pd.DataFrame) -> pd.Series:
    times = pd.DataFrame(
        data={'usertype': dataset['usertype'],
              'starttime': dataset['starttime']}
    )
    times['starttime'] = times['starttime'].dt.date
    return times.value_counts()


# 获取各群体每日使用单车次数，用于'gender',一级检索为0='unknown',1='male',2='womale',
def count_times_gender(data: pd.DataFrame) -> pd.Series:
    times = pd.DataFrame(
        data={'gender': data['gender'],
              'starttime': data['starttime']}
    )
    times['starttime'] = times['starttime'].dt.date
    return times.value_counts()


# 获取各群体每日使用单车次数，用于'birth year',一级检索为'少年','青年','中年','老年'
def count_times_birth(data: pd.DataFrame, current: int) -> pd.Series:
    times = pd.DataFrame(
        data={'birth year': data['birth year'],
              'starttime': data['starttime']}
    )
    times['starttime'] = times['starttime'].dt.date
    times['group'] = pd.cut(
        x=times['birth year'].map(lambda x: current-x),
        bins=[0, 19, 45, 70, 91],
        labels=['少年', '青年', '中年', '老年'],
        right=False)
    times.dropna(axis=0, how='any', inplace=True)
    times.drop(columns=['birth year'], inplace=True)
    return times.groupby(by='group').value_counts()


# 绘制当年不同群体单车使用频率的热力日历图
def drawCalendar(dataset_201903: pd.DataFrame, dataset_202003: pd.DataFrame) -> Calendar:
    usertype_201903 = count_times_usertype(dataset_201903)
    gender_201903 = count_times_gender(dataset_201903)
    birth_201903 = count_times_birth(dataset_201903, 2019)
    usertype_202003 = count_times_usertype(dataset_202003)
    gender_202003 = count_times_gender(dataset_202003)
    birth_202003 = count_times_birth(dataset_202003, 2020)
    max_ = max(usertype_201903.describe()[
               'max'], usertype_202003.describe()['max'])
    min_ = max(usertype_201903.describe()[
               'min'], usertype_202003.describe()['min'])
    calendar = (
        Calendar()
        .add(
            series_name='subscriber',
            yaxis_data=[[label, value, normalize(value, max_, min_)]
                        for label, value in usertype_201903['Subscriber'].items()],
            is_selected=False,
        )
        .add(
            series_name='customer',
            yaxis_data=[[label, value, normalize(value, max_, min_)]
                        for label, value in usertype_201903['Customer'].items()],
            is_selected=False,
        )
        .add(
            series_name='male',
            yaxis_data=[[label, value, normalize(value, max_, min_)]
                        for label, value in gender_201903[1].items()],
            is_selected=False,
        )
        .add(
            series_name='womale',
            yaxis_data=[[label, value, normalize(value, max_, min_)]
                        for label, value in gender_201903[2].items()],
            is_selected=False,
        )
        .add(
            series_name='unknown',
            yaxis_data=[[label, value, normalize(value, max_, min_)]
                        for label, value in gender_201903[0].items()],
            is_selected=False,
        )
        .add(
            series_name='少年',
            yaxis_data=[[label, value, normalize(value, max_, min_)]
                        for label, value in birth_201903['少年'].items()],
            is_selected=False,
        )
        .add(
            series_name='青年',
            yaxis_data=[[label, value, normalize(value, max_, min_)]
                        for label, value in birth_201903['青年'].items()],
            is_selected=False,
        )
        .add(
            series_name='中年',
            yaxis_data=[[label, value, normalize(value, max_, min_)]
                        for label, value in birth_201903['中年'].items()],
            is_selected=False,
        )
        .add(
            series_name='老年',
            yaxis_data=[[label, value, normalize(value, max_, min_)]
                        for label, value in birth_201903['老年'].items()],
            is_selected=False,
        )
    )
    calendar.add(
        series_name='subscriber',
        yaxis_data=[[label, value, normalize(value, max_, min_)]
                    for label, value in usertype_202003['Subscriber'].items()],
        is_selected=False,
    )
    calendar.add(
        series_name='customer',
        yaxis_data=[[label, value, normalize(value, max_, min_)]
                    for label, value in usertype_202003['Customer'].items()],
        is_selected=False,
    )
    calendar.add(
        series_name='male',
        yaxis_data=[[label, value, normalize(value, max_, min_)]
                    for label, value in gender_202003[1].items()],
        is_selected=False,
    )
    calendar.add(
        series_name='womale',
        yaxis_data=[[label, value, normalize(value, max_, min_)]
                    for label, value in gender_202003[2].items()],
        is_selected=False,
    )
    calendar.add(
        series_name='unknown',
        yaxis_data=[[label, value, normalize(value, max_, min_)]
                    for label, value in gender_202003[0].items()],
        is_selected=False,
    )
    calendar.add(
        series_name='少年',
        yaxis_data=[[label, value, normalize(value, max_, min_)]
                    for label, value in birth_202003['少年'].items()],
        is_selected=False,
    )
    calendar.add(
        series_name='青年',
        yaxis_data=[[label, value, normalize(value, max_, min_)]
                    for label, value in birth_202003['青年'].items()],
        is_selected=False,
    )
    calendar.add(
        series_name='中年',
        yaxis_data=[[label, value, normalize(value, max_, min_)]
                    for label, value in birth_202003['中年'].items()],
        is_selected=False,
    )
    calendar.add(
        series_name='老年',
        yaxis_data=[[label, value, normalize(value, max_, min_)]
                    for label, value in birth_202003['老年'].items()],
        is_selected=False,
        calendar_opts=[
            opts.CalendarOpts(range_='2019-03', pos_top='17%',
                              daylabel_opts=opts.CalendarDayLabelOpts(name_map='cn', margin=10)),
            opts.CalendarOpts(range_='2020-03', pos_bottom='17%',
                              daylabel_opts=opts.CalendarDayLabelOpts(name_map='cn', margin=10)),
        ],
    )
    calendar.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            max_=1,
            min_=0,
            range_text=[str(int(max_)), str(int(min_))],
            pos_top='bottom',
            pos_left='right',
            orient='horizontal',
        ),
        tooltip_opts=opts.TooltipOpts(
            hide_delay=50,
            formatter=JsCode(
                """
                    function(params) {
                        return 'Date: ' + params.value[0]
                            + '<br/>Times: ' + params.value[1];
                    }
                """
            ),
        ),
        legend_opts=opts.LegendOpts(pos_top='3%'),
    )
    return calendar
