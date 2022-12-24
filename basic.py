import os

import pandas as pd
from pyecharts.charts import Tab, Timeline

import basic_analysis.drawCalendar as dC
import basic_analysis.drawLine as dL
import basic_analysis.drawPie as dP
from basic_analysis.drawBMap import *


# 绘制时间轮播图
def drawTimeline(sInfo: pd.DataFrame, filepath: str) -> Timeline:
    #!需在timeline对应div末尾script处手动加入
    # var bmap = {chartName}.getModel().getComponent('bmap').getBMap();
    # bmap.addControl(new BMap.NavigationControl({"anchor": 0, "offset": {"width": 10, "height": 10}, "type": 0, "showZoomInfo": false, "enableGeolocation": false}));
    total = pd.read_csv(filepath)
    max_ = total['count'].max()
    min_ = total['count'].min()
    timeline = Timeline()
    timeline.add_schema(
        pos_left='center',
        pos_bottom='15px',
        width='700px',
        symbol_size=5,
    )
    for i in range(1, 32):
        try:
            dirname = os.path.dirname(filepath)
            basename = os.path.basename(filepath)
            folder = dirname+'/detail/'+basename.split('.')[0]+'/'
            bmap = traffic.drawSingle(
                sInfo, folder+str(i)+'.csv', max_, min_)
            timeline.add(bmap, {'value': 'day='+str(i),
                                'tooltip': {'formatter': '{b}'}})
        except FileNotFoundError:
            print('day='+str(i)+' has not traffic info file!')
    return timeline


# 绘制tab页面
def drawTab(data_201903: pd.DataFrame, data_202003: pd.DataFrame) -> None:
    tab = Tab()
    tab.add(dL.drawGrid(data_201903, data_202003), '借车量折线图')
    tab.add(dP.drawGrid(data_201903, data_202003), '分类占比图')
    tab.add(dC.drawCalendar(data_201903, data_202003), '不同群体使用频率图')
    siteInfo_201903 = pd.read_csv('data/siteInfo/201903.csv')
    siteInfo_202003 = pd.read_csv('data/siteInfo/202003.csv')
    tab.add(sites.drawScatter(siteInfo_201903, siteInfo_202003), '站点分布图')
    tab.add(drawTimeline(siteInfo_201903,
            'data/trafficInfo/201903.csv'), '201903站点流量时间轮播图')
    tab.add(drawTimeline(siteInfo_202003,
            'data/trafficInfo/202003.csv'), '202003站点流量时间轮播图')
    tab.render('preliminary.html')


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


if __name__ == '__main__':
    data201903 = load('data/clear/201903.csv')
    data202003 = load('data/clear/202003.csv')
    drawTab(data201903, data202003)
