import json
import os

import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import BMap
from pyecharts.commons.utils import JsCode


# 获取BMap站点配置文件
def get_config_json(data: pd.DataFrame, savepath: str) -> pd.DataFrame:
    config = pd.DataFrame(data={
        'id': data['sID'],
        'name': data['sName'],
        'coord': list(zip(data['sLongitude'], data['sLatitude']))
    }).set_index('name')
    dirname = os.path.dirname(savepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    config.loc[:, 'coord'].to_json(path_or_buf=savepath, orient='index')
    return config


# 绘制站点分布图
def drawScatter(siteInfo_201903: pd.DataFrame, siteInfo_202003: pd.DataFrame) -> BMap:
    config_201903 = get_config_json(
        siteInfo_201903, 'static/json/config_201903.json')
    config_202003 = get_config_json(
        siteInfo_202003, 'static/json/config_202003.json')
    with open('static/json/map_style.json', 'r', encoding='utf-8') as fp:
        map_style = json.load(fp)
    bmap = (
        BMap(init_opts=opts.InitOpts(
            animation_opts=opts.AnimationOpts(animation=False)))
        .add_schema(
            baidu_ak='M98sRd8ltiZpeQRi8w3QtqZGN0I56MdD',
            center=[-73.97999825, 40.72219576],
            zoom=14,
            is_roam=False,
            map_style=map_style,
        )
        .add_coordinate_json('static/json/config_201903.json')
        .add_coordinate_json('static/json/config_202003.json')
        .add(
            series_name='2019',
            type_='scatter',
            data_pair=list(zip(config_201903.index, config_201903['id'])),
            symbol='circle',
            is_large=True,
            is_selected=False,
            tooltip_opts=opts.TooltipOpts(
                trigger_on='click',
                axis_pointer_type='shadow',
                hide_delay=50,
                formatter=JsCode(
                    """
                        function(params) {
                            if ('value' in params.data) {
                                return 'SiteName: ' + params.data.name
                                    + '<br/>ID: ' + params.data.value[2]
                                    + '<br/>Coordinate: (' + params.data.value[0]
                                    +','+ params.data.value[1]+')';
                            }
                        }
                    """
                ),
            ),
        )
        .add(
            series_name='2020',
            type_='scatter',
            data_pair=list(zip(config_202003.index, config_202003['id'])),
            symbol='circle',
            is_large=True,
            is_selected=False,
            tooltip_opts=opts.TooltipOpts(
                trigger_on='click',
                axis_pointer_type='shadow',
                hide_delay=50,
                formatter=JsCode(
                    """
                        function(params) {
                            if ('value' in params.data) {
                                return 'SiteName: ' + params.data.name
                                    + '<br/>ID: ' + params.data.value[2]
                                    + '<br/>Coordinate: (' + params.data.value[0]
                                    +','+ params.data.value[1]+')';
                            }
                        }
                    """
                ),
            ),
        )
        .add_control_panel(
            navigation_control_opts=opts.BMapNavigationControlOpts(),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .add_js_funcs(
            """
                function loadStyle(url) {
                    var link = document.createElement('link');
                    link.type = 'text/css';
                    link.rel = 'stylesheet';
                    link.href = url;
                    var head = document.getElementsByTagName('head')[0];
                    head.appendChild(link);
                }
                loadStyle('static/css/display.css');
            """
        )
    )
    return bmap
