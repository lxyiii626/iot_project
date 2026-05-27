# influx_sensor.py
# 传感器数据同时发送到 MQTT 和 InfluxDB

import random
import time
import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# MQTT 配置
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/data"

# InfluxDB 配置
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "j0kIw2hxGQTSLbhDvOAvme9uD5OMsRTkYsP2XLA-ZplH39UjmmT4UTRa-xK8TPo6Dp0keWSIudadcPASww4Lzw=="
INFLUXDB_ORG = "myorg"
INFLUXDB_BUCKET = "mybucket"

class Sensor:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        # MQTT 客户端
        self.mqtt_client = mqtt.Client()
        # InfluxDB 客户端
        self.influx_client = InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG
        )
        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
    
    def connect_mqtt(self):
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print(f"MQTT 已连接: {MQTT_BROKER}:{MQTT_PORT}")
    
    def generate_data(self):
        temperature = random.uniform(20.0, 35.0)
        humidity = random.uniform(30.0, 80.0)
        light = random.randint(0, 1000)
        
        return {
            "sensor_id": self.sensor_id,
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "light": light,
            "timestamp": time.time()
        }
    
    def save_to_influxdb(self, data):
        point = Point("environment") \
            .tag("sensor_id", data["sensor_id"]) \
            .field("temperature", data["temperature"]) \
            .field("humidity", data["humidity"]) \
            .field("light", data["light"]) \
            .time(int(data["timestamp"] * 1_000_000_000))
        
        self.write_api.write(bucket=INFLUXDB_BUCKET, record=point)
        print(f"已存入 InfluxDB: {data['temperature']}°C, {data['humidity']}%, {data['light']}lux")
    
    def run(self):
        self.connect_mqtt()
        print(f"{self.sensor_id} 启动成功")
        
        while True:
            data = self.generate_data()
            
            # 发送到 MQTT
            payload = json.dumps(data)
            self.mqtt_client.publish(MQTT_TOPIC, payload)
            print(f"MQTT 已发送: {payload}")
            
            # 保存到 InfluxDB
            self.save_to_influxdb(data)
            
            time.sleep(5)

if __name__ == "__main__":
    sensor = Sensor("sensor_001")
    sensor.run()