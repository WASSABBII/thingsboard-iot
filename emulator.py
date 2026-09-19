import requests
import time
import math
import random

TB_URL = "http://localhost:8080"
TOKEN = "foDOp2t3GFYLqy54BIcq"


temp_supply = 18.0      # в
temp_outdoor = -5.0     # nт
temp_setpoint = 22.0    # u
filter_pressure = 50.0  # pa
humidity = 45.0         # bl %
fan_supply_rpm = 1500   # ob1
fan_exhaust_rpm = 1400  # ob2
damper_pos = 100.0      
heat_valve = 0.0     
cool_valve = 0.0       
is_running = True
is_alarm = False
filter_clogged = False

tick = 0

def send_telemetry(data):
    url = f"{TB_URL}/api/v1/{TOKEN}/telemetry"
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"✅ Отправлено: {data}")
    else:
        print(f"❌ Ошибка: {response.status_code}")

print("работает")

while True:
    tick += 1

    # Температура подтягивается к уставке
    diff = temp_setpoint - temp_supply
    heat_valve = max(0, min(100, diff * 5))
    cool_valve = max(0, min(100, -diff * 5))
    temp_supply += diff * 0.05 + random.uniform(-0.2, 0.2)

    # nt  меняется медленно
    temp_outdoor += random.uniform(-0.1, 0.1)

    # Фильтр постепенно засоряется
    filter_pressure += random.uniform(0.05, 0.15)
    if filter_pressure > 250:
        filter_clogged = True
        is_alarm = True
    else:
        filter_clogged = False
        is_alarm = False

    # ob
    fan_supply_rpm = 1500 + random.randint(-50, 50)
    fan_exhaust_rpm = 1400 + random.randint(-50, 50)

    # b
    humidity += random.uniform(-0.3, 0.3)
    humidity = max(20, min(80, humidity))

    data = {
        "temp_supply": round(temp_supply, 1),
        "temp_outdoor": round(temp_outdoor, 1),
        "temp_setpoint": temp_setpoint,
        "fan_supply_rpm": fan_supply_rpm,
        "fan_exhaust_rpm": fan_exhaust_rpm,
        "filter_pressure_diff": round(filter_pressure, 1),
        "damper_position": damper_pos,
        "heat_valve": round(heat_valve, 1),
        "cool_valve": round(cool_valve, 1),
        "humidity": round(humidity, 1),
        "is_running": is_running,
        "is_alarm": is_alarm,
        "filter_clogged": filter_clogged
    }

    send_telemetry(data)
    time.sleep(5)
