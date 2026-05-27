from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
from influxdb_client import InfluxDBClient

app = Flask(__name__)
CORS(app)

INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "j0kIw2hxGQTSLbhDvOAvme9uD5OMsRTkYsP2XLA-ZplH39UjmmT4UTRa-xK8TPo6Dp0keWSIudadcPASww4Lzw=="
INFLUXDB_ORG = "myorg"
INFLUXDB_BUCKET = "mybucket"

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>环境监测系统</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
    <style>
        body { font-family: Arial; margin: 20px; background: #f0f2f5; }
        h1 { text-align: center; }
        .chart-box { background: white; padding: 15px; margin: 20px auto; width: 800px; border-radius: 10px; }
        .latest { text-align: center; margin: 20px auto; padding: 15px; background: white; border-radius: 10px; width: 800px; }
        .value { font-size: 24px; margin: 0 20px; }
        button { padding: 10px 20px; font-size: 16px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🌡️ 环境监测系统</h1>
    <div class="latest">
        <span class="value temp">🌡️ 温度: --°C</span>
        <span class="value humi">💧 湿度: --%</span>
        <span class="value light">☀️ 光照: --lux</span>
        <button onclick="refresh()">🔄 刷新</button>
    </div>
    <div class="chart-box"><div id="chart" style="height:400px;"></div></div>
    <script>
        var chart;
        function refresh() {
            fetch('/api/data')
                .then(res => res.json())
                .then(data => {
                    document.querySelector('.temp').innerHTML = `🌡️ 温度: ${data.latest.temp}°C`;
                    document.querySelector('.humi').innerHTML = `💧 湿度: ${data.latest.humi}%`;
                    document.querySelector('.light').innerHTML = `☀️ 光照: ${data.latest.light}lux`;
                    
                    if(!chart) chart = echarts.init(document.getElementById('chart'));
                    chart.setOption({
                        tooltip: { trigger: 'axis' },
                        xAxis: { type: 'category', data: data.times },
                        yAxis: { type: 'value', name: '数值' },
                        series: [
                            { name: '温度', type: 'line', data: data.temps, color: '#ff6b6b' },
                            { name: '湿度', type: 'line', data: data.humis, color: '#4ecdc4' },
                            { name: '光照', type: 'line', data: data.lights, color: '#ffe66d' }
                        ]
                    });
                });
        }
        refresh();
        setInterval(refresh, 5000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/data')
def get_data():
    query = f'from(bucket:"{INFLUXDB_BUCKET}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "environment")'
    result = client.query_api().query(query)
    
    times, temps, humis, lights = [], [], [], []
    latest = {'temp': 0, 'humi': 0, 'light': 0}
    point_map = {}
    
    for table in result:
        for record in table.records:
            t = record.get_time().strftime('%H:%M:%S')
            if t not in point_map:
                point_map[t] = {}
            field = record.get_field()
            value = record.get_value()
            point_map[t][field] = value
            if field == 'temperature':
                latest['temp'] = value
            elif field == 'humidity':
                latest['humi'] = value
            elif field == 'light':
                latest['light'] = value
    
    for t in sorted(point_map.keys())[-30:]:
        times.append(t)
        temps.append(point_map[t].get('temperature', 0))
        humis.append(point_map[t].get('humidity', 0))
        lights.append(point_map[t].get('light', 0))
    
    return jsonify({'times': times, 'temps': temps, 'humis': humis, 'lights': lights, 'latest': latest})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)