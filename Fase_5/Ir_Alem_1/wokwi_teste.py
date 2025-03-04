import network
import time
from machine import Pin
import dht
import urequests
import ntptime

def connect_to_wifi():
    print("Connecting to WiFi", end="\n")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Wokwi-GUEST', '')  # Replace with your WiFi SSID
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print("\nConnected to WiFi:", sta_if.isconnected(), "IP Address:", sta_if.ifconfig()[0])

def get_current_time_iso():
    tm = time.localtime()
    year, month, day, hour, minute, second, weekday, yearday = tm
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z".format(year, month, day, hour, minute, second)

connect_to_wifi()
ntptime.settime()  # Synchronize the clock with NTP
sensor = dht.DHT22(Pin(15))

api_url = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras/"
prev_value = ""

while True:
    print("Measuring weather conditions... ", end="\n")
    sensor.measure()
    humidity = sensor.humidity()
    dt = get_current_time_iso()
    if humidity != prev_value:
        message = f'{{"data_leitura": "{dt}", "sensor": "DHT22", "valor": {humidity}}}'
        print("Reporting to Server:", message)
        headers = {"Content-Type": "application/json"}
        try:
            response = urequests.post(api_url, headers=headers, data=message)
            if response.status_code == 201:
                response_json = response.json()
                print("Created ID:", response_json.get("id"))
                print("Data successfully posted to the server!")
            else:
                print("Failed to post data. Status code:", response.status_code)
            response.close()
        except Exception as e:
            print("Error:", e)
        prev_value = humidity
    time.sleep(5)