const option_bmap = {
    "animation": false,
    "animationThreshold": 2000,
    "animationDuration": 1000,
    "animationEasing": "cubicOut",
    "animationDelay": 0,
    "animationDurationUpdate": 300,
    "animationEasingUpdate": "cubicOut",
    "animationDelayUpdate": 0,
    "color": [
        "#c23531",
        "#2f4554",
        "#61a0a8",
        "#d48265",
        "#749f83",
        "#ca8622",
        "#bda29a",
        "#6e7074",
        "#546570",
        "#c4ccd3",
        "#f05b72",
        "#ef5b9c",
        "#f47920",
        "#905a3d",
        "#fab27b",
        "#2a5caa",
        "#444693",
        "#726930",
        "#b2d235",
        "#6d8346",
        "#ac6767",
        "#1d953f",
        "#6950a1",
        "#918597"
    ],
    "legend": [
        {
            "data": [
                "Inter",
                "Intra",
                "cluster",
            ],
            "selected": {
                "Inter": true,
                "Intra": true,
                "cluster": true,
            },
            "show": true,
            "left": "right",
            "top": "top",
            "orient": "vertical",
            "align": "left",
            "padding": 5,
            "itemGap": 10,
            "itemWidth": 25,
            "itemHeight": 14
        }
    ],
    "tooltip": {
        "show": false,
        "trigger": "item",
        "triggerOn": "mousemove|click",
        "axisPointer": {
            "type": "line"
        },
        "showContent": true,
        "alwaysShowContent": false,
        "showDelay": 0,
        "hideDelay": 100,
        "formatter": function (params) {
            return 'Outer';
        },
        "textStyle": {
            "fontSize": 14
        },
        "borderWidth": 0,
        "padding": 5
    },
    "title": [
        {
            "padding": 5,
            "itemGap": 10
        }
    ],
    "visualMap": {
        "show": true,
        "type": "continuous",
        "min": 0,
        "max": 1,
        "inRange": {
            "color": [
                '#6ab92c',
                '#aed606',
                '#fef804',
                '#db253e',
                '#db253e',
                '#5b1875',
            ],
            "symbolSize": [0, 1],
        },
        "outOfRange": {
            "color": 'black',
            "opacity": 0,
        },
        "controller": {
            "inRange": {
                "symbolSize": [30, 100]
            }
        },
        "calculable": true,
        "inverse": false,
        "splitNumber": 5,
        "orient": "vertical",
        "showLabel": true,
        "itemWidth": 20,
        "itemHeight": 140,
        "borderWidth": 0
    },
    "bmap": {
        "center": [
            -73.97999825,
            40.72219576
        ],
        "zoom": 14,
        "roam": false,
        "mapStyle": function () {
            // const post = "http://127.0.0.1:5501/";
            // let api = post + "static/json/map_style.json";
            let api = "../../static/json/map_style.json";
            let jsonData;
            $.ajax({
                url: api,
                type: 'GET',
                dataType: 'json',
                async: false,
                success: (data) => {
                    jsonData = data;
                },
                error: (e) => {
                    console.log(e);
                },
            });
            return jsonData;
        }(),
    }
};
let backup_series_data;

$(function () {
    const chart_bmap = echarts.init(document.getElementById('bmap'), 'white', { renderer: 'canvas' });
    updateBMap([], [], []);
    document.getElementById('date').addEventListener('change', getData, false);
    document.querySelector('#trafficFilter button').addEventListener('click', get_trafficFilter, false);
    chart_bmap.on('click', function (params) {
        if (params.seriesIndex == 1) {
            let obj = ReadCSV().find(o => o.clusterID == params.data[2]);
            alert('Cluster ' + params.data[2] + ' contains the following site:\n' + obj.stationID);
            let record = ReadJSON().find(o => o.from == params.data[2] && o.to == params.data[2]);
            let detail = [];
            for (i = 0; i < record['detail_trip'].length; i++) {
                detail.push(record['detail_trip'][i]['from'] + '->' + record['detail_trip'][i]['to']
                    + ':' + record['detail_trip'][i]['count']);
            }
            document.querySelector('#detail div.content').innerHTML = 'The intra-class traffic for cluster '
                + params.data[2] + ' is ' + params.data[3]
                + '\nDetail infomation as follows: (station ID)\n' + detail;
        } else {
            let obj1 = ReadCSV().find(o => o.clusterID == params.data[4]);
            let obj2 = ReadCSV().find(o => o.clusterID == params.data[5]);
            alert('Cluster ' + params.data[4] + ' contains the following site:\n' + obj1.stationID
                + '\n\nCluster ' + params.data[5] + ' contains the following site:\n' + obj2.stationID);
            let record = ReadJSON().find(o => o.from == params.data[4] && o.to == params.data[5]);
            let detail = [];
            for (i = 0; i < record['detail_trip'].length; i++) {
                detail.push(record['detail_trip'][i]['from'] + '->' + record['detail_trip'][i]['to']
                    + ':' + record['detail_trip'][i]['count']);
            }
            document.querySelector('#detail div.content').innerHTML = 'The interclass traffic from cluster '
                + params.data[4] + ' to cluster ' + params.data[5] + ' is ' + params.data[6]
                + '\nDetail infomation as follows: (station ID)\n' + detail;
        }
    });

    function get_trafficFilter() {
        let min_tmp = document.getElementById('min_value').value;
        // let max_tmp = document.getElementById('max_value').value;
        if (chart_bmap.getOption().series.length == 0) {
            alert('Please select a date first!');
        }
        // else if (min_tmp.length == 0 || max_tmp.length == 0 || parseInt(min_tmp) > parseInt(max_tmp)) {
        //     alert('The traffic selector gets an incorrect range!');
        // }
        else if (min_tmp.length == 0) {
            alert('Enter the lowest value for filtered traffic!');
        }
        else if (parseInt(min_tmp) <= 0) {
            alert('The traffic filter gets a non-positive value!');
        }
        else {
            option_bmap.visualMap.min = parseInt(min_tmp);
            // option_bmap.visualMap.max = parseInt(max_tmp);
            let InterData = backup_series_data[0].filter((item, index) => {
                // return item[6] >= min_tmp && item[6] <= max_tmp;
                return item[6] >= min_tmp;
            });
            let IntraData = backup_series_data[1].filter((item, index) => {
                // return item[3] >= min_tmp && item[3] <= max_tmp;
                return item[3] >= min_tmp;
            });
            updateBMap(InterData, IntraData, backup_series_data[2]);
        }
    }

    /**
     * 
     * @param {array} InterData 
     * @param {array} IntraData 
     * @param {array} clusterData 
     */
    function updateBMap(InterData, IntraData, clusterData) {
        let series = [
            {
                "type": "custom",
                "name": "Inter",
                "coordinateSystem": "bmap",
                "renderItem": function (params, api) {
                    const coord1 = api.coord([
                        api.value(0, params.dataIndexInside),
                        api.value(1, params.dataIndexInside),
                    ]);
                    const coord2 = api.coord([
                        api.value(2, params.dataIndexInside),
                        api.value(3, params.dataIndexInside),
                    ]);
                    let [arcPoints, mid_id] = getArcPoints(coord1[0], coord1[1], coord2[0], coord2[1], 500, 0.5);
                    let arrowPoints = getArrowPoints(
                        arcPoints[mid_id - 1][0], arcPoints[mid_id - 1][1],
                        arcPoints[mid_id][0], arcPoints[mid_id][1],
                        Math.PI / 6,
                    )
                    let polylines = [];
                    polylines.push({
                        type: 'polyline',
                        name: 'arc',
                        shape: {
                            points: arcPoints,
                        },
                        style: {
                            fill: 'rgba(0, 0, 0, 0)',
                            stroke: api.visual('color'),
                            lineWidth: 1 + api.visual('symbolSize') * 9,
                        },
                        z2: api.visual('symbolSize') + 50,
                    });
                    polylines.push({
                        type: 'polyline',
                        name: 'arrow',
                        shape: {
                            points: arrowPoints,
                        },
                        style: {
                            fill: 'rgba(0, 0, 0, 0)',
                            stroke: api.visual('color'),
                            lineWidth: 5 + api.visual('symbolSize') * 18,
                        },
                        z2: api.visual('symbolSize') + 50,
                    });
                    return {
                        type: 'group',
                        children: [...polylines],
                    };
                },
                "data": InterData,
                "emphasis": {},
                "label": {
                    "show": false,
                },
                "rippleEffect": {
                    "show": true,
                    "brushType": "stroke",
                    "scale": 2.5,
                    "period": 4
                },
            },
            {
                "type": "custom",
                "name": "Intra", // ????
                "coordinateSystem": "bmap",
                "renderItem": function (params, api) {
                    const coord = api.coord([
                        api.value(0, params.dataIndexInside),
                        api.value(1, params.dataIndexInside),
                    ]);
                    let rings = [];
                    rings.push({
                        type: 'ring',
                        shape: {
                            cx: coord[0],
                            cy: coord[1],
                            r0: 2,
                            r: 6,
                        },
                        style: {
                            fill: api.visual('color'),
                            stroke: 'rgba(0,0,0,0)',
                            lineWidth: 0.1,
                        },
                        z2: api.visual('symbolSize') + 100,
                    });
                    return {
                        type: 'group',
                        children: [...rings],
                    };
                },
                "emphasis": {},
                "data": IntraData,
                "label": {
                    "show": false,
                },
                "rippleEffect": {
                    "show": true,
                    "brushType": "stroke",
                    "scale": 2.5,
                    "period": 4
                },
            },
            {
                "type": "custom",
                "name": "cluster", // ???
                "coordinateSystem": "bmap",
                "renderItem": function (params, api) {
                    const coord = api.coord([
                        api.value(0, params.dataIndexInside),
                        api.value(1, params.dataIndexInside),
                    ]);
                    let circles = [];
                    circles.push({
                        type: 'circle',
                        shape: {
                            cx: coord[0],
                            cy: coord[1],
                            r: 2,
                        },
                        style: {
                            fill: 'black',
                        },
                        z2: api.visual('symbolSize') + 150,
                    });
                    return {
                        type: 'group',
                        children: [...circles],
                    };
                },
                "emphasis": {},
                "data": clusterData,
                "label": {
                    "show": false,
                },
                "rippleEffect": {
                    "show": true,
                    "brushType": "stroke",
                    "scale": 2.5,
                    "period": 4
                },
                "tooltip": {
                    "show": true,
                    "trigger": "item",
                    "triggerOn": "mousemove|click",
                    "axisPointer": {
                        "type": "line"
                    },
                    "showContent": true,
                    "alwaysShowContent": false,
                    "showDelay": 0,
                    "hideDelay": 100,
                    "formatter": function (params) {
                        return 'Cluster ' + params.data[2];
                    },
                    "textStyle": {
                        "fontSize": 14
                    },
                    "borderWidth": 0,
                    "padding": 5
                },
            },
        ];
        chart_bmap.clear();
        chart_bmap.setOption(option_bmap);
        chart_bmap.getModel().getComponent('bmap').getBMap().addControl(
            new BMap.NavigationControl({
                "anchor": 0,
                "offset": {
                    "width": 10,
                    "height": 10
                },
                "type": 0,
                "showZoomInfo": false,
                "enableGeolocation": false,
            })
        );
        if (InterData.length != 0 && IntraData.length != 0) {
            chart_bmap.setOption({ "series": series });
        }
    }

    function getData() {
        try {
            const data = ReadJSON();
            if (typeof (data) == 'undefined') {
                throw new Error('undefined data!');
            }
            const clusterInfo = ReadCSV();
            if (typeof (clusterInfo) == 'undefined') {
                throw new Error('undefined clusterInfo!');
            }
            alert('Valid date. Please wait for a moment.');
            option_bmap.visualMap.min = Math.min.apply(null, data.map(item => { return item.count }));;
            option_bmap.visualMap.max = Math.max.apply(null, data.map(item => { return item.count }));;
            document.getElementById('max_value').value = option_bmap.visualMap.max;
            let InterData = [], IntraData = [];
            for (let i = 0; i < data.length; i++) {
                let record = data[i];
                if (record.from == record.to) {
                    let obj = clusterInfo.find(o => o.clusterID == record.from);
                    IntraData.push([
                        obj.cLongitude,
                        obj.cLatitude,
                        obj.clusterID,
                        record.count,
                    ]);
                } else {
                    let obj1 = clusterInfo.find(o => o.clusterID == record.from);
                    let obj2 = clusterInfo.find(o => o.clusterID == record.to);
                    InterData.push([
                        obj1.cLongitude,
                        obj1.cLatitude,
                        obj2.cLongitude,
                        obj2.cLatitude,
                        obj1.clusterID,
                        obj2.clusterID,
                        record.count,
                    ]);
                }
            }
            backup_series_data = [];
            backup_series_data.push(InterData);
            backup_series_data.push(IntraData);
            backup_series_data.push(clusterInfo.map((value, index, array) => {
                return [value.cLongitude, value.cLatitude, value.clusterID];
            }));
            updateBMap(backup_series_data[0], backup_series_data[1], backup_series_data[2]);
            alert('BMap has been updated.');
        }
        catch (e) {
            option_bmap.visualMap.min = 0;
            option_bmap.visualMap.max = 1;
            document.getElementById('max_value').value = option_bmap.visualMap.max;
            updateBMap([], [], []);
            console.log(e);
            alert('Error');
        }
    }

})

/**
 * 
 * @returns {object}
 */
function ReadCSV() {
    const date = document.getElementById('date').textContent;
    // const post = "http://127.0.0.1:5501/";
    let year = date.split('-')[0];
    // let api = post + "data/clusterInfo/" + year + ".csv";
    let api = "../../data/clusterInfo/" + year + ".csv";
    let jsonData;
    $.ajax({
        url: api,
        type: 'GET',
        dataType: 'text',
        async: false,
        success: (data) => {
            jsonData = $.csv.toObjects(data);
        },
        error: (e) => {
            alert('There is no cluster Info!');
        },
    });
    return jsonData;
}

/**
 * 
 * @returns {object}
 */
function ReadJSON() {
    const date = document.getElementById('date').textContent;
    // const post = "http://127.0.0.1:5501/";
    let year = date.split('-')[0];
    let month = date.split('-')[1];
    // let api = post + "data/cluster_ST/" + year + month + ".json";
    let api = "../../data/cluster_ST/" + year + month + ".json";
    let jsonData;
    $.ajax({
        url: api,
        type: "GET",
        dataType: "json",
        async: false,
        success: (data) => {
            jsonData = data[date];
        },
        error: (e) => {
            alert('There is no data for this month!');
        },
    });
    return jsonData;
}

/**
 * 
 * @param {Number} x1 
 * @param {Number} y1 
 * @param {Number} x2 
 * @param {Number} y2 
 * @param {Number} pointCount 
 * @param {Number} level 
 * @returns {[array,Number]} [points, mid_id]
 * @refer https://blog.csdn.net/kingviewer/article/details/120346353?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-9-120346353-blog-103735361.pc_relevant_3mothn_strategy_recovery&spm=1001.2101.3001.4242.6&utm_relevant_index=12
 */
function getArcPoints(x1, y1, x2, y2, pointCount, level) {
    let a, b, rSquare, k, kv;
    let points = [], mid_id, min_distance_delta = 9999;
    if (x1 === x2) {
        a = x1 + (y2 - y1) * level;
        b = y1 + (y2 - y1) / 2;
        rSquare = (x1 - a) ** 2 + (y1 - b) ** 2;
    } else if (y1 === y2) {
        a = x1 + (x2 - x1) / 2;
        b = y1 - (x2 - x1) * level;
        rSquare = (x1 - a) ** 2 + (y1 - b) ** 2;
    } else {
        let xc = (x1 + x2) / 2, yc = (y1 + y2) / 2,
            lenSquare = ((x2 - x1) ** 2 + (y2 - y1) ** 2) * (level ** 2);
        k = (x2 - x1) / (y1 - y2);
        let l = yc - k * xc;
        let a1 = 1 + k ** 2,
            b1 = 2 * k * (l - yc) - 2 * xc,
            c1 = xc ** 2 + (l - yc) ** 2 - lenSquare;
        kv = -1 / k;
        a = (-b1 + Math.sqrt(b1 ** 2 - 4 * a1 * c1) * ((kv > 0 && x2 > x1 || kv < 0 && x2 < x1) ? 1 : -1)) / (2 * a1);
        b = k * a + l;
        rSquare = (x1 - a) ** 2 + (y1 - b) ** 2;
    }
    if (x1 === x2 || Math.abs(kv) > 1) {
        let yDistance = y2 - y1;
        let yDis = yDistance / (pointCount + 1);
        for (let i = 0; i < pointCount; i++) {
            let y = y1 + yDis * (i + 1);
            let x = Math.sqrt(rSquare - (y - b) ** 2) * (y2 > y1 ? -1 : 1) + a;
            points.push([x, y]);
            let distance_delta = Math.abs(Math.sqrt((x - x1) ** 2 + (y - y1) ** 2) - Math.sqrt((x - x2) ** 2 + (y - y2) ** 2));
            if (distance_delta < min_distance_delta) {
                min_distance_delta = distance_delta;
                mid_id = i;
            }
        }
    } else {
        let xDistance = x2 - x1;
        let xDis = xDistance / (pointCount + 1);
        for (let i = 0; i < pointCount; i++) {
            let x = x1 + xDis * (i + 1);
            let y = Math.sqrt(rSquare - (x - a) ** 2) * (x2 > x1 ? 1 : -1) + b;
            points.push([x, y]);
            let distance_delta = Math.abs(Math.sqrt((x - x1) ** 2 + (y - y1) ** 2) - Math.sqrt((x - x2) ** 2 + (y - y2) ** 2));
            if (distance_delta < min_distance_delta) {
                min_distance_delta = distance_delta;
                mid_id = i;
            }
        }
    }
    return [points, mid_id];
}

/**
 * 
 * @param {Number} x1 
 * @param {Number} y1 
 * @param {Number} x2 
 * @param {Number} y2 
 * @param {Number} alpha 
 * @returns {array} points
 * @refer https://blog.csdn.net/csxiaoshui/article/details/65446125 
 */
function getArrowPoints(x1, y1, x2, y2, alpha) {
    let points = [];
    function getRMatrix(x2, y2, alpha) {
        let R_alpha = math.matrix([
            [Math.cos(alpha), Math.sin(alpha), 0],
            [-Math.sin(alpha), Math.cos(alpha), 0],
            [(1 - Math.cos(alpha)) * x2 + y2 * Math.sin(alpha), (1 - Math.cos(alpha)) * y2 - x2 * Math.sin(alpha), 1],
        ]);
        return R_alpha;
    }
    let ori = math.matrix([x1, y1, 1]);
    let m1 = math.multiply(ori, getRMatrix(x2, y2, alpha));
    let m2 = math.multiply(ori, getRMatrix(x2, y2, -alpha));
    points.push(math.subset(m1, math.index([0, 1]))._data);
    points.push([x2, y2]);
    points.push(math.subset(m2, math.index([0, 1]))._data);
    return points;
}
