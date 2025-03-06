from machine import Pin, ADC
from time import sleep
import dht
import network
import urequests
import json
import time
import ntptime

# Configurações Wi-Fi
print("Conectando-se ao Wi-Fi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Conectado!")

# Aguarda a conexão com timeout
timeout = 10  # segundos
while not sta_if.isconnected() and timeout > 0:
    print("Conectando ao Wi-Fi...")
    time.sleep(1)
    timeout -= 1

if sta_if.isconnected():
    print("Conectado ao Wi-Fi!")
    print("Endereço IP:", sta_if.ifconfig()[0])
else:
    print("Falha na conexão Wi-Fi")

# Configurações do sensor DHT22
pino_dht = Pin(15)
sensor_dht = dht.DHT22(pino_dht)

# Configurações do sensor LDR
pino_ldr = Pin(34)
ldr = ADC(pino_ldr)
ldr.atten(ADC.ATTN_11DB)

def get_current_time_iso():
    tm = time.localtime()
    year, month, day, hour, minute, second, weekday, yearday = tm
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z".format(year, month, day, hour, minute, second)

def enviar_dados_api(sensor, valor):
    # Preparar dados para enviar para a API
    data = {
        "data_leitura": dt,
        "sensor": sensor,
        "valor": valor,
    }

    # Enviar dados via POST para a API
    response = urequests.post(url_api, headers=headers, json=data)

    # Verificar resposta da API
    if response.status_code == 201:
        print("Dados enviados com sucesso para a API.")
    else:
        print("Erro ao enviar dados para a API:", response.status_code)
        print(response.text)

    response.close()  # Importante fechar a resposta

# Configurações da API Oracle
url_api = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras/"
headers = {"Content-Type": "application/json"}

temperatura_ant = None
lux_ant = None

try:
    ntptime.settime()
    print("Tempo sincronizado com NTP.")
except OSError as e:
    print("Erro ao sincronizar tempo com NTP:", e)

while True:
    try:
        # Leitura do sensor DHT
        sensor_dht.measure()
        temperatura = sensor_dht.temperature()

        # Leitura do sensor LDR
        lux = ldr.read()
        
        # Data da leitura
        dt = get_current_time_iso()

        # Mostrar leituras
        print("Temperatura:", temperatura, "°C, Luminosidade:", lux, "lux")

        # Enviar dados pro banco
        if (temperatura is not None and temperatura != temperatura_ant):
            enviar_dados_api("DHT22", temperatura)
            temperatura_ant = temperatura

        if (lux is not None and lux != lux_ant):
            enviar_dados_api("LDR", lux)
            lux_ant = lux

    except OSError as e:
        print("Erro de leitura do sensor:", e)
    except Exception as e:
        print("Ocorreu um erro:", e)

    sleep(3)
