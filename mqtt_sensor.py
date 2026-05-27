# mqtt_sensor.py
# 通过 MQTT 发送传感器数据

import random
import time
import json
import paho.mqtt.client as mqtt

# MQTT 配置
MQTT_BROKER = "localhost"  # 本机 Mosquitto 服务器
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/data"

class MQTTSensor:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.client = mqtt.Client()
    
    def connect(self):
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print(f"已连接到 MQTT 服务器: {MQTT_BROKER}:{MQTT_PORT}")
    
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
    
    def run(self):
        self.connect()
        print(f"{self.sensor_id} 启动成功，开始发送数据...")
        
        while True:
            data = self.generate_data()
            payload = json.dumps(data)  # 转成 JSON 字符串
            self.client.publish(MQTT_TOPIC, payload)
            print(f"已发送: {payload}")
            time.sleep(5)

if __name__ == "__main__":
    sensor = MQTTSensor("sensor_001")
    sensor.run()