import requests
import time
import math
import random

TB_URL = "http://localhost:8080"
TOKEN = "foDOp2t3GFYLqy54BIcq"

# Начальные значения
temp_supply = 18.0      # Температура приточного воздуха
temp_outdoor = -5.0     # Наружная температура
temp_setpoint = 22.0    # Уставка
filter_pressure = 50.0  # Перепад давления на фильтре (Па)
humidity = 45.0         # Влажность %
fan_supply_rpm = 1500   # Обороты приточного вентилятора
fan_exhaust_rpm = 1400  # Обороты вытяжного вентилятора
damper_pos = 100.0      # Положение заслонки %
heat_valve = 0.0        # Клапан нагрева %
cool_valve = 0.0        # Клапан охлаждения %
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

print("🚀 Эмулятор ПВУ запущен...")

while True:
    tick += 1

    # Температура подтягивается к уставке
    diff = temp_setpoint - temp_supply
    heat_valve = max(0, min(100, diff * 5))
    cool_valve = max(0, min(100, -diff * 5))
    temp_supply += diff * 0.05 + random.uniform(-0.2, 0.2)

    # Наружная температура меняется медленно
    temp_outdoor += random.uniform(-0.1, 0.1)

    # Фильтр постепенно засоряется
    filter_pressure += random.uniform(0.05, 0.15)
    if filter_pressure > 250:
        filter_clogged = True
        is_alarm = True
    else:
        filter_clogged = False
        is_alarm = False

    # Обороты вентиляторов
    fan_supply_rpm = 1500 + random.randint(-50, 50)
    fan_exhaust_rpm = 1400 + random.randint(-50, 50)

    # Влажность
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
