import requests, json, paho.mqtt.client as mqtt
client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
client.connect("broker.hivemq.com", 1883, 60)
weather_url = "https://api.open-meteo.com/v1/forecast?latitude=10.0159&longitude=76.3419&current=temperature_2m,relative_humidity_2m,weather_code"
air_url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=10.0159&longitude=76.3419&current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone,european_aqi"
weather = requests.get(weather_url).json()
air = requests.get(air_url).json()
data = {
    "temperature": weather["current"]["temperature_2m"],
    "humidity": weather["current"]["relative_humidity_2m"],
    "pm10": air["current"]["pm10"],
    "pm25": air["current"]["pm2_5"],
    "aqi": air["current"]["european_aqi"]
}
client.publish("environment/data", json.dumps(data))
print("Data Published:", data)
client.disconnect()