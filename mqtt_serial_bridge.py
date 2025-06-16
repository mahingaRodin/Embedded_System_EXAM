import serial
import paho.mqtt.client as mqtt
import json
import time

# Configuration
SERIAL_PORT = 'COM4'
BAUD_RATE = 9600
MQTT_BROKER = '157.173.101.159'
MQTT_PORT = 1883
SENSOR_TOPIC = 'sensor/data'
LED_TOPIC = 'climateControl'

# Serial setup
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with code {rc}")
    client.subscribe(LED_TOPIC)
    print(f"Subscribed to {LED_TOPIC}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        if 'led' in data:
            ser.write((payload + '\n').encode('utf-8'))
            print(f"Sent to Arduino: {payload}")
    except Exception as e:
        print(f"Error processing message: {e}")

# MQTT client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# Main loop
while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    json.loads(line)
                    client.publish(SENSOR_TOPIC, line)
                    print(f"Published to {SENSOR_TOPIC}: {line}")
                except json.JSONDecodeError:
                    print(f"Invalid JSON: {line}")
        time.sleep(0.1)  # Prevent CPU overload
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)  # Wait before retrying