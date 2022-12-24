$(function () {
    const chart_calendar = echarts.init(document.getElementById('calendar'), 'white', { renderer: 'canvas' });
    document.querySelectorAll("#calendarPicker button").forEach(button => {
        button.addEventListener('click', (params) => {
            let year = params.target.textContent;
            initCalendar(year, year + '-03-01', year + '-08-31');
        }, false);
    })

    /**
     * 
     * @param {string} year 
     */
    function initCalendar(year) {
        let option_calendar = {
            "animation": true,
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
            "series": [
                {
                    "type": "heatmap",
                    "coordinateSystem": "calendar",
                    "data": function (year) {
                        // const post = "http://127.0.0.1:5501/";
                        // let api = post + "data/cluster_T/" + year + ".csv";
                        let api = "../../data/cluster_T/" + year + ".csv";
                        let res = [];
                        $.ajax({
                            url: api,
                            type: 'GET',
                            dataType: 'text',
                            async: false,
                            success: (data) => {
                                let jsonData = $.csv.toObjects(data);
                                res = res.concat(Array.from(jsonData, row => [row["date"], row["label"]]));
                            },
                            error: (e) => {
                                console.log(e);
                                alert('There is no cluster_T Info about ' + year + '!');
                            },
                        });
                        return res;
                    }(year),
                    "label": {
                        "show": true,
                        "position": "top",
                        "margin": 8
                    }
                },
            ],
            "legend": [
                {
                    "data": [
                        ""
                    ],
                    "selected": {
                        "": true
                    },
                    "show": true,
                    "top": "3%",
                    "padding": 5,
                    "itemGap": 10,
                    "itemWidth": 25,
                    "itemHeight": 14
                }
            ],
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
                "textStyle": {
                    "fontSize": 14
                },
                "borderWidth": 0,
                "padding": 5,
                "formatter": (params) => { return params.data[0]; },
            },
            "calendar": {
                "width": "auto",
                "orient": "horizontal",
                "range": year,
                "cellSize": 20,
                "dayLabel": {
                    "show": true,
                    "firstDay": 1,
                    "margin": 10,
                    "position": "start",
                    "nameMap": ['Sun', 'Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat'],
                    "color": "#000",
                    "fontStyle": "normal",
                    "fontWeight": "normal",
                    "fontFamily": "sans-serif",
                    "fontSize": 12
                },
                "yearLabel": {
                    "position": "top",
                },
            },
            "visualMap": {
                "show": false,
                "type": "piecewise",
                "calculable": true,
                "inverse": false,
                "splitNumber": 5,
                "orient": "horizontal",
                "left": "right",
                "top": "bottom",
                "showLabel": true,
                "itemWidth": 20,
                "itemHeight": 14,
                "borderWidth": 0,
                "pieces": [
                    {
                        "value": 0,
                        "color": "#91CB74"
                    },
                    {
                        "value": 1,
                        "color": "#73C0DE"
                    },
                    {
                        "value": 2,
                        "color": "#FAC858"
                    },
                    {
                        "value": 3,
                        "color": "#EE6666"
                    }
                ]
            }
        };
        chart_calendar.clear();
        chart_calendar.setOption(option_calendar);
    }
})
