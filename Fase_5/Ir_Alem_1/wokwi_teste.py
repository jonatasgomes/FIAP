import network
import time
from machine import Pin
import dht
import urequests

sensor = dht.DHT22(Pin(15))

def connect_to_wifi():
    print("Connecting to WiFi", end="\n")
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

prev_value = ""
while True:
    print("Measuring weather conditions... ", end="\n")
    sensor.measure()  # temperature = sensor.temperature()
    humidity = sensor.humidity()
    dt = "2025-02-27T13:16:36.333Z"
    message = f'{{"data_leitura": "{dt}", "sensor": "DHT22", "valor": {humidity}}}'
    
    if humidity != prev_value:
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
        prev_value = humidity
    
    time.sleep(5)
