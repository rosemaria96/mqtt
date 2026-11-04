import streamlit as st
import paho.mqtt.client as mqtt
import json
from supabase import create_client
st.title("MQTT Environmental Monitoring Dashboard")
SUPABASE_URL = "https://agyfixwqrrhdxtcxzkzb.supabase.co"
SUPABASE_KEY = "sb_publishable_u1pfE8gCUEB9Z_SEJ6hFfg_o0gcnwvv"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
if st.button("Get Environmental Data"):
    received = {}
    def on_connect(client, userdata, flags, reason_code, properties):
        client.subscribe("environment/data")
    def on_message(client, userdata, msg):
        received.update(json.loads(msg.payload.decode()))
        client.disconnect()
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)
    client.loop_forever()
    if received:
        supabase.table("environment").insert(received).execute()
        st.success("Data received and stored successfully!")
        col1, col2 = st.columns(2)
        col1.metric("Temperature", str(received["temperature"]) + " °C")
        col2.metric("Humidity", str(received["humidity"]) + " %")
        col3, col4, col5 = st.columns(3)
        col3.metric("PM10", received["pm10"])
        col4.metric("PM2.5", received["pm25"])
        col5.metric("AQI", received["aqi"])
st.header("Cloud Database Records")
result = supabase.table("environment").select("*").execute()
st.dataframe(result.data)
