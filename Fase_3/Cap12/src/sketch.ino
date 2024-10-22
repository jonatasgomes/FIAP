#include <DHT.h> // biblioteca do sensor DHT22

#define SR04_TRIG_PIN 32 // pino TRIG do sensor ultrassom HC-SR04
#define SR04_ECHO_PIN 35 // pino ECHO do sensor ultrassom HC-SR04
#define RELAY1_IN_PIN 33 // pino IN do relé para bomba d'agua
#define DHT22_SDA_PIN 25 // pino SDA do sensor de umidade/temperatura DHT22
#define DHT22_MODEL DHT22 // tipo do sensor DHT22
#define RELAY2_IN_PIN 26 // pino IN do relé para irrigacao

const int alturaReservatorio = 400; // altura do reservatorio de agua em cm
DHT dht(DHT22_SDA_PIN, DHT22_MODEL);

// inicializacao e configuracao da placa e pinos
void setup() {
  Serial.begin(115200); // inicializar comunicacao serial
  pinMode(SR04_TRIG_PIN, OUTPUT); // setar pino como saida/escrita
  pinMode(SR04_ECHO_PIN, INPUT); // setar pino como entrada/leitura
  pinMode(RELAY1_IN_PIN, OUTPUT); // setar pino como saida/escrita
  pinMode(RELAY2_IN_PIN, OUTPUT); // setar pino como saida/escrita
  dht.begin(); // inicializar sensor DHT22
}

// loop principal
void loop() {
  monitorarNivelAgua(); // monitorar nivel de agua no reservatorio e ligar/desligar bomba d'agua
  monitorarTemperaturaUmidade(); // monitorar temperatura e umidade e ligar/desligar irrigacao
  delay(500); // Wait for 2 seconds before taking another reading
}

// usar sensor HC-SR04 para medir nivel de agua e usar relé para ligar/desligar bomba d'agua
void monitorarNivelAgua() {
  // enviar pulso a partir do sensor HC-SR04
  digitalWrite(SR04_TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(SR04_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(SR04_TRIG_PIN, LOW);
  // medir tempo de retorno do pulso
  long pulso = pulseIn(SR04_ECHO_PIN, HIGH);
  // calcular distancia em cm entre o sensor no topo e o nivel de agua abaixo
  int distancia = pulso * 0.034 / 2;
  // calcular nivel de agua no reservatorio
  int nivel = map(distancia, 0, alturaReservatorio, 100, 0);
  // mostrar nivel
  Serial.println("Nivel de agua: " + String(nivel) + "%.");
  // controlar bomba de agua para manter reservatorio em torno de 80% cheio
  if (nivel < 80) {
    digitalWrite(RELAY1_IN_PIN, HIGH); // ligar bomba de agua
    Serial.println("Bomba de agua ligada.");
  } else if (nivel >= 80) {
    digitalWrite(RELAY1_IN_PIN, LOW); // desligar bomba de agua
    Serial.println("Bomba de agua desligada.");
  }
}

// usar sensor DHT22 para medir temperatura e umidade e usar relé para ligar/desligar irrigacao
void monitorarTemperaturaUmidade() {
  float umid = dht.readHumidity(); // ler umidade
  float temp = dht.readTemperature(); // ler temperatura
  if (isnan(umid) || isnan(temp)) { // checar se leitura esta valida
    Serial.println("Erro ao ler do sensor DHT22.");
    return;
  }
  Serial.println("Umidade: " + String(umid) + "%.");
  Serial.println("Temperatura: " + String(temp) + "ºC.");
  if (umid < 40 || temp > 30) {
    digitalWrite(RELAY2_IN_PIN, HIGH); // ligar irrigacao
    Serial.println("Irrigação ligada.");
  } else {
    digitalWrite(RELAY2_IN_PIN, LOW); // desligar irrigacao
    Serial.println("Irrigação desligada.");
  }
}