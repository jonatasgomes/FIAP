import network
import time
from machine import Pin
import dht
import ujson
import urequests

sensor = dht.DHT22(Pin(15))

def connect_to_wifi():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Wokwi-GUEST', '')
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print("Connected to WiFi:", sta_if.isconnected())
    print("IP Address:", sta_if.ifconfig()[0])

connect_to_wifi()
api_url = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras/"

prev_weather = ""
while True:
    print("Measuring weather conditions... ", end="")
    sensor.measure()
    humidity = sensor.humidity() # temperature = sensor.temperature()
    payload = {
        "data_leitura": "2025-02-27T13:16:36.333Z",
        "sensor": "DHT22",
        "valor": humidity
    }
    message = ujson.dumps(payload)
    
    if message != prev_weather:
        print("Reporting to Server:", message)
        headers = {"Content-Type": "application/json"}
        try:
            response = urequests.post(api_url, headers=headers, data=message)
            if response.status_code == 201:
                print("Response Status Code:", response.status_code)
                print("Response Content:", response.text)
                print("Data successfully posted to the server!")
            else:
                print("Failed to post data. Status code:", response.status_code)
            response.close()
        except Exception as e:
            print("Error:", e)
        prev_weather = message
    
    time.sleep(5)
