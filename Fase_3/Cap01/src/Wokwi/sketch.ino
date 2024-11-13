// importar bibliotecas
#include <WiFi.h>
#include "time.h"
#include <DHT.h>

// dados do wifi
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// dados do ntp
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = -18000;
const int daylightOffset_sec = 0;

// dados dos pinos
const int pino_potassio = 23;
int potassio = LOW;
const int pino_fosforo = 34;
int fosforo = LOW;
const int pino_dht = 32;
float umidade;
const int pino_ldr = 15;
float ph;
const int pino_rele = 2;

// sensor DHT
DHT dht(pino_dht, DHT22);

// dados auxiliares
String leitura = "";
int irrigacao = LOW;

// intervalo de tempo para exibir leituras (2 minutos)
unsigned long previousMillis = 0;
const long interval = 120000;  // 2 minutos em milissegundos

// inicializar a placa
void setup() {
  Serial.begin(115200);

  // conectar wifi
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Connected!");

  // inicializar ntp
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  Serial.println("NTP Initialized!");

  // inicializar pinos
  pinMode(pino_potassio, INPUT);
  pinMode(pino_fosforo, INPUT);
  pinMode(pino_ldr, INPUT);
  pinMode(pino_rele, OUTPUT);

  // inicializar sensor dht
  dht.begin();

  // esperar inicialização completar
  delay(1000);

}

// loop principal
void loop() {
  // ler potássio
  ler_potassio();

  // ler fósforo
  ler_fosforo();

  // ler umidade
  ler_umidade();

  // ler ph
  ler_ph();

  // verificar se passaram 2 minutos para mostrar a nova leitura e checar irrigacao
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;  // atualizar o tempo da última execução
    mostrar_leitura();
    checar_irrigacao();
  }

  // esperar 0,05 segundos para não sobrecarregar o loop
  delay(50);
}

// retorna data e hora
String ler_data_hora() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return "Failed to obtain time";
  }
  String formattedDateTime = String(timeinfo.tm_mday) + "-" +
                             String(timeinfo.tm_mon + 1) + "-" +
                             String(timeinfo.tm_year + 1900) + " " +
                             (timeinfo.tm_hour < 10 ? "0" : "") + String(timeinfo.tm_hour) + ":" +
                             (timeinfo.tm_min < 10 ? "0" : "") + String(timeinfo.tm_min) + ":" +
                             (timeinfo.tm_sec < 10 ? "0" : "") + String(timeinfo.tm_sec);
  
  return formattedDateTime;
}

// ler potássio
void ler_potassio() {
  int _potassio = digitalRead(pino_potassio);
  _potassio = _potassio == HIGH ? 100 : 0;
  if (_potassio != potassio) {
    potassio = _potassio;
  }
}

// ler fósforo
void ler_fosforo() {
  int _fosforo = digitalRead(pino_fosforo);
  _fosforo = _fosforo == HIGH ? 100 : 0;
  if (_fosforo != fosforo) {
    fosforo = _fosforo;
  }
}

// ler umidade
void ler_umidade() {
  float _umidade = dht.readHumidity();
  if (_umidade != umidade) {
    umidade = _umidade;
  }
}

// ler ph
void ler_ph() {
  int _analog = analogRead(pino_ldr); // Usando analogRead para ler valores entre 0 e 1023
  float _ph = map(_analog, 0, 1023, 0, 14); // Converte o valor para a escala de pH de 0 a 14
  if (_ph != ph) {
    ph = _ph;
  }
}

// mostrar leitura
void mostrar_leitura() {
  leitura = "{'data_hora': '" + String(ler_data_hora()) + "', 'potassio': '" +
    String(potassio) + "', 'fosforo': '" + String(fosforo) + "', 'umidade': '" +
    String(umidade) + "', 'ph': '" + String(ph) + "'}";
  Serial.println(leitura);
}

// checar se precisa ligar/desligar irrigação
void checar_irrigacao() {
  // se irrigação está ligada
  if (irrigacao == HIGH) {
    // desligar irrigação se umidade maior que 120
    if (umidade > 120) {
      digitalWrite(pino_rele, LOW);
      irrigacao = LOW;
    }
  } else { // irrigação está desligada
    // ligar irrigação se umidade menor que 100
    if (umidade < 100) {
      digitalWrite(pino_rele, HIGH);
      irrigacao = HIGH;
    }
  }
}