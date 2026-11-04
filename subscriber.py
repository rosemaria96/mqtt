import paho.mqtt.client as mqtt
import json
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT Broker")
    client.subscribe("environment/data")
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("Received Environmental Data")
    print("Temperature:", data["temperature"])
    print("Humidity:", data["humidity"])
    print("PM10:", data["pm10"])
    print("PM2.5:", data["pm25"])
    print("AQI:", data["aqi"])
client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()
