# sensor_simulator.py
# 模拟传感器，每5秒生成温度、湿度、光照数据

import random
import time

class Sensor:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
    
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
        print(f"{self.sensor_id} 启动成功")
        while True:
            data = self.generate_data()
            print(data)
            time.sleep(5)

if __name__ == "__main__":
    sensor = Sensor("sensor_001")
    sensor.run()