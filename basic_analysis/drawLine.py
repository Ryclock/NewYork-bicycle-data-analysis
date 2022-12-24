import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Grid, Line
from pyecharts.commons.utils import JsCode


# 分别统计工作日和周末的自行车每小时平均被借量
def lentNum_perHour(dataset: pd.DataFrame, info: str) -> pd.DataFrame:
    df = pd.DataFrame(
        index=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
               '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],
    )
    tmp = pd.DataFrame(dataset['starttime'])
    tmp['hour'] = dataset['starttime'].dt.hour
    tmp['group'] = pd.cut(
        x=dataset['starttime'].dt.dayofweek,
        bins=[0, 5, 7],
        labels=['workday', 'weekend'],
        right=False)
    tmp.dropna(axis=0, how='any', inplace=True)
    count_2019 = tmp.groupby(by=['group', 'hour']).count()
    df['workday'+info] = count_2019.loc['workday', 'starttime'].values
    df['weekend'+info] = count_2019.loc['weekend', 'starttime'].values
    workdays = len(pd.bdate_range(info+'01', info+'31'))
    weekends = len(pd.bdate_range(info+'01', info+'31', freq='d'))-workdays
    df['workday'+info] = df['workday'+info].map(lambda x: x/workdays)
    df['weekend'+info] = df['weekend'+info].map(lambda x: x/weekends)
    return df


# 绘制自行车每小时平均借车量关系图
def drawLine_perHour(total: pd.DataFrame) -> Line:
    line = (
        Line()
        .add_xaxis(
            xaxis_data=total.index.tolist(),
        )
        .add_yaxis(
            series_name='201903工作日借车量',
            y_axis=total['workday201903'].values.tolist(),
            symbol='emptyCircle',
            is_symbol_show=True,
            is_connect_nones=True,
            color='#FF9158',
        )
        .add_yaxis(
            series_name='201903周末借车量',
            y_axis=total['weekend201903'].values.tolist(),
            symbol='rect',
            is_symbol_show=True,
            is_connect_nones=True,
            color='#FF9158',
        )
        .add_yaxis(
            series_name='202003工作日借车量',
            y_axis=total['workday202003'].values.tolist(),
            symbol='emptyCircle',
            is_symbol_show=True,
            is_connect_nones=True,
            color='#58E8FF',
        )
        .add_yaxis(
            series_name='202003周末借车量',
            y_axis=total['weekend202003'].values.tolist(),
            symbol='rect',
            is_symbol_show=True,
            is_connect_nones=True,
            color='#58E8FF',
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                is_silent=True,
                data=[opts.MarkLineItem(name='平均值', type_='average')],
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger='item',
                axis_pointer_type='cross',
                formatter=JsCode(
                    """
                        function(params) {
                            return params.value[0]+'时: '+params.value[1];
                        }
                    """
                ),
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='每小时平均借车量',
                pos_left='center',
            ),
            xaxis_opts=opts.AxisOpts(type_='category'),
            yaxis_opts=opts.AxisOpts(
                name='借车量',
                type_='value',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            legend_opts=opts.LegendOpts(
                pos_left='center',
                orient='horizontal',
                pos_top='5%',
            )
        )
    )
    return line


# 统计自行车每日被借量
def lentNum_perDay(dataset_201903: pd.DataFrame, dataset_202003: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(
        index=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
               '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
               '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'],
    )
    df['201903'] = dataset_201903['starttime'].dt.day.value_counts().sort_index().values
    df['202003'] = dataset_202003['starttime'].dt.day.value_counts().sort_index().values
    return df


# 绘制自行车每日借车量关系图
def drawLine_perDay(total: pd.DataFrame) -> Line:
    line = (
        Line()
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='每日借车量',
                pos_left='center',
                pos_top='50%',
            ),
            xaxis_opts=opts.AxisOpts(type_='category'),
            yaxis_opts=opts.AxisOpts(
                name='借车量',
                type_='value',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            legend_opts=opts.LegendOpts(
                pos_left='center',
                orient='horizontal',
                pos_top='55%',
            )
        )
        .add_xaxis(
            xaxis_data=total.index.tolist(),
        )
        .add_yaxis(
            series_name='201903',
            y_axis=total['201903'].values.tolist(),
            symbol='emptyCircle',
            is_symbol_show=True,
            is_connect_nones=True,
            color='#FF9158',
        )
        .add_yaxis(
            series_name='202003',
            y_axis=total['202003'].values.tolist(),
            symbol='emptyCircle',
            is_symbol_show=True,
            is_connect_nones=True,
            color='#58E8FF',
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                is_silent=True,
                data=[opts.MarkLineItem(name='平均值', type_='average')],
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger='item',
                axis_pointer_type='cross',
                formatter=JsCode(
                    """
                        function(params) {
                            return params.value[0]+'号: '+params.value[1];
                        }
                    """
                ),
            ),
        )
    )
    return line


# 绘制并行折线图
def drawGrid(dataset_201903: pd.DataFrame, dataset_202003: pd.DataFrame) -> Grid:
    # 每小时借车量
    lent_hour_total = pd.concat([
        lentNum_perHour(dataset_201903, '201903'),
        lentNum_perHour(dataset_202003, '202003')
    ], axis=1)
    grid = (
        Grid()
        .add(drawLine_perHour(lent_hour_total), grid_opts=opts.GridOpts(pos_bottom='58%'))
        .add(drawLine_perDay(lentNum_perDay(dataset_201903, dataset_202003)),
             grid_opts=opts.GridOpts(pos_top='62%'))
    )
    return grid
