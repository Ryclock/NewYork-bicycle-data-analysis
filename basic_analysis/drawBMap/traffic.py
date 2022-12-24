import json

import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import BMap
from pyecharts.commons.utils import JsCode


# 获取某天各站点的流量信息
def get_traffic_day(sInfo: pd.DataFrame, filepath: str) -> pd.DataFrame:
    traffic = pd.DataFrame(data={
        'id': sInfo['sID'],
        'longitude': sInfo['sLongitude'],
        'latitude': sInfo['sLatitude'],
    })
    data = pd.read_csv(filepath)
    traffic['start'] = traffic['id'].map(
        lambda id: sum(data.query('sID_start==@id')['count']))
    traffic['stop'] = traffic['id'].map(
        lambda id: sum(data.query('sID_end==@id')['count']))
    traffic['all'] = traffic['start']+traffic['stop']
    return traffic.drop(index=traffic.query('all==0').index)


# 绘制单张流量图
def drawSingle(sInfo: pd.DataFrame, filepath: str, max_: int, min_: int) -> BMap:
    current = get_traffic_day(sInfo, filepath)
    with open('static/json/map_style.json', 'r', encoding='utf-8') as fp:
        map_style = json.load(fp)
    bmap = (
        BMap()
        .add_schema(
            baidu_ak='M98sRd8ltiZpeQRi8w3QtqZGN0I56MdD',
            center=[-73.97999825, 40.72219576],
            zoom=14,
            is_roam=False,
            map_style=map_style,
        )
        .add(
            series_name='all',
            type_='custom',
            data_pair=[list(z) for z in zip(
                current['longitude'], current['latitude'], current['start'], current['stop'], current['all'])],
            # custom的tooltip_opts失效,目前尝试只能通过这种方式添加
            render_item=JsCode(
                """
                    function (params, api) {
                        const coord = api.coord([api.value(0, params.dataIndexInside), api.value(1, params.dataIndexInside)]);
                        const start = api.value(2, params.dataIndexInside);
                        const stop = api.value(3, params.dataIndexInside);
                        const sectors = [];
                        sectors.push({
                            type: 'sector',
                            shape: {
                                cx: coord[0],
                                cy: coord[1],
                                r: api.visual('symbolSize'),
                                r0: 0,
                                startAngle: - Math.PI / 2,
                                endAngle: - Math.PI / 2 + Math.PI * 2 * (start / (start + stop)),
                                transition:[],
                            },
                            z2: start + stop,
                            style: {
                                fill: 'red',
                            },
                        });
                        sectors.push({
                            type: 'sector',
                            shape: {
                                cx: coord[0],
                                cy: coord[1],
                                r: api.visual('symbolSize'),
                                r0: 0,
                                startAngle: - Math.PI / 2 + Math.PI * 2 * (start / (start + stop)),
                                endAngle: Math.PI * 3 / 2,
                                transition:[],
                            },
                            z2: start + stop,
                            style: {
                                fill: 'blue',
                            },
                        });
                        return {
                            type: 'group',
                            children: [...sectors],
                        };
                    },
                    tooltip: {
                        show: true,
                        trigger: 'item',
                        triggerOn: 'mousemove|click',
                        axisPointer: {
                            type: 'line'
                        },
                        showContent: true,
                        alwaysShowContent: false,
                        showDelay: 0,
                        hideDelay: 100,
                        formatter:
                            function (params) {
                                return 'total: ' + params.data[4]
                                    + '<br/>' + 'start: ' + params.data[2]
                                    + '<br/>' + 'stop: ' + params.data[3];
                            },
                        textStyle: {
                            fontSize: 14
                        },
                        borderWidth: 0,
                        padding: 5
                    }
                """
            ),
        )
        .add_control_panel(
            navigation_control_opts=opts.BMapNavigationControlOpts(),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=[
                opts.VisualMapOpts(
                    type_='size',
                    max_=max_,
                    min_=min_,
                    range_size=[1, 5],
                    pos_top='center',
                    pos_left='left',
                    series_index=0,
                    is_show=False,
                ),
            ],
            tooltip_opts=opts.TooltipOpts(is_show=False),
        )
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
