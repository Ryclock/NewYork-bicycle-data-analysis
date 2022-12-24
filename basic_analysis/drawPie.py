import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Grid, Pie


# 获取某维度各分类占比情况，用于'usertype'
def get_classPercent_usertype(data: pd.DataFrame) -> pd.Series:
    return data['usertype'].value_counts()


# 获取某维度各分类占比情况，用于'gender'
def get_classPercent_gender(data: pd.DataFrame) -> pd.Series:
    return data['gender'].value_counts().rename(index={1: 'male', 2: 'womale', 0: 'unknown'})


# 获取某维度各分类占比情况，用于'birth year'
def get_classPercent_birth(data: pd.DataFrame, current: int) -> pd.Series:
    frame = data['birth year'].value_counts().rename_axis(
        'birth year').to_frame('times')
    frame['group'] = pd.cut(
        x=frame.index.map(lambda x: current-x),
        bins=[0, 19, 45, 70, 91],
        labels=['少年(0-18)', '青年(19-44)', '中年(45-69)', '老年(70-90)'],
        right=False)
    frame.dropna(axis=0, how='any', inplace=True)
    sum = frame.groupby(by='group').sum()
    percent = pd.Series(data=sum['times'], index=sum.index)
    return percent


# 绘制2019年的所有分类占比图（垂直放置）
def drawPie_2019(dataset: pd.DataFrame) -> Pie:
    data_usertype = get_classPercent_usertype(dataset)
    data_gender = get_classPercent_gender(dataset)
    data_birth = get_classPercent_birth(dataset, 2019)
    pie = (
        Pie(
            init_opts=opts.InitOpts(width='200px', height='650px')
        )
        .add(
            series_name='usertype',
            data_pair=[list(z)for z in zip(
                data_usertype.index.tolist(), data_usertype.values.tolist())],
            center=['25%', 150],
            radius=[40, 80],
        )
        .add(
            series_name='gender',
            data_pair=[list(z)for z in zip(
                data_gender.index.tolist(), data_gender.values.tolist())],
            center=['25%', 350],
            radius=[40, 80],
        )
        .add(
            series_name='birth',
            data_pair=[list(z)for z in zip(
                data_birth.index.tolist(), data_birth.values.tolist())],
            center=['25%', 550],
            radius=[40, 80],
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='201903各维度分类占比图',
                pos_left='left',
            ),
            legend_opts=opts.LegendOpts(
                is_show=True,
                pos_left='center',
                orient='vertical',
                align='left',
            ),
        )
    )
    return pie


# 绘制2020年的所有分类占比图（垂直放置）
def drawPie_2020(dataset: pd.DataFrame) -> Pie:
    data_usertype = get_classPercent_usertype(dataset)
    data_gender = get_classPercent_gender(dataset)
    data_birth = get_classPercent_birth(dataset, 2020)
    pie = (
        Pie(
            init_opts=opts.InitOpts(height='650px')
        )
        .add(
            series_name='usertype',
            data_pair=[list(z)for z in zip(
                data_usertype.index.tolist(), data_usertype.values.tolist())],
            center=['75%', 150],
            radius=[40, 80],
        )
        .add(
            series_name='gender',
            data_pair=[list(z)for z in zip(
                data_gender.index.tolist(), data_gender.values.tolist())],
            center=['75%', 350],
            radius=[40, 80],
        )
        .add(
            series_name='birth',
            data_pair=[list(z)for z in zip(
                data_birth.index.tolist(), data_birth.values.tolist())],
            center=['75%', 550],
            radius=[40, 80],
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='202003各维度分类占比图',
                pos_left='right',
            ),
            legend_opts=opts.LegendOpts(
                is_show=True,
                pos_left='center',
                orient='vertical',
                align='left',
            ),
        )
    )
    return pie


# 绘制并行饼图
def drawGrid(dataset_201903: pd.DataFrame, dataset_202003: pd.DataFrame) -> Grid:
    grid = (
        Grid(init_opts=opts.InitOpts(height='650px'))
        .add(drawPie_2019(dataset_201903), grid_opts=opts.GridOpts(pos_left='left'))
        .add(drawPie_2020(dataset_202003), grid_opts=opts.GridOpts(pos_left='right'))
    )
    return grid
