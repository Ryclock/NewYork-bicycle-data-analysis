import json
import random

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import BMap
from pyecharts.commons.utils import JsCode


def randomcolors(n:int)-> list:
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    colors = []
    for i in range(n):
        color = "#"
        for i in range(6):
            color += colorArr[random.randint(0,14)]
        if color not in colors:
            colors.append(color)
        else:
            i -= 1
    return colors


def drawSites_cluster(data:pd.DataFrame,cluster_key:str,max_:int,min_:int) -> BMap:
    with open('static/json/map_style.json', 'r', encoding='utf-8') as fp:
        map_style = json.load(fp)
    bmap = (
            BMap(init_opts=opts.InitOpts(
            width='900px',
            height='500px',
            animation_opts=opts.AnimationOpts(animation=False),
        ))
        .add_schema(
            baidu_ak='M98sRd8ltiZpeQRi8w3QtqZGN0I56MdD',
            center=[-73.97999825, 40.72219576],
            zoom=14,
            is_roam=False,
            map_style=map_style,
        )
        .add(
            series_name=cluster_key,
            type_='custom',
            is_selected=False,
            data_pair=[list(z) for z in zip(data['longitude'], data['latitude'], data['siteName'],data[cluster_key])],
            # custom的tooltip_opts失效,目前尝试只能通过这种方式添加
            render_item=JsCode(
                """
                    function (params, api) {
                        const coord = api.coord([api.value(0, params.dataIndexInside), api.value(1, params.dataIndexInside)]);
                        const circles = [];
                        circles.push({
                            type: 'circle',
                            shape: {
                                cx: coord[0],
                                cy: coord[1],
                                r: 5,
                            },
                            style: {
                                fill: api.visual('color'),
                            },
                        });
                        return {
                            type: 'group',
                            children: [...circles],
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
                                return  'Site: '+ params.data[2]
                                    +'</br> Label: '+ params.data[3];
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
            navigation_control_opts=opts.BMapNavigationControlOpts())
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(
                is_show=True,
                pos_left='right',
                pos_top='top',
                orient='vertical',
                align='left',
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,
                min_=min_,
                max_=max_,
                range_color=randomcolors(max_-min_+1),
            )
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

    