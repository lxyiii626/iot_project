# 物联网云边协同监控系统

基于 MQTT + InfluxDB + Flask + ECharts 的物联网数据采集与可视化系统。

## 功能特点

- 模拟多传感器数据源（温度、湿度、光照）
- MQTT 协议传输数据
- InfluxDB 时序数据库存储
- Flask 提供 RESTful API
- ECharts 实时图表展示

## 技术栈

- Python
- MQTT (Mosquitto)
- InfluxDB
- Flask
- ECharts

## 运行方法

1. 启动 Mosquitto：`mosquitto -v`
2. 启动 InfluxDB：双击 `influxd.exe`
3. 运行传感器：`python influx_sensor.py`
4. 运行 Web 服务器：`python web_server.py`
5. 浏览器访问：`http://127.0.0.1:5000`

## 项目截图

<img width="415" height="212" alt="image" src="https://github.com/user-attachments/assets/c23f397b-6146-45c8-97e7-68a25bc0b547" />
<img width="415" height="214" alt="image" src="https://github.com/user-attachments/assets/66d4fec5-6619-4507-90cf-247513d5ce38" />



## 作者

李向阳
