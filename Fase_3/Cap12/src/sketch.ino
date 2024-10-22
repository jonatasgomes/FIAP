#define SR04_TRIG_PIN 32 // pino TRIG do sensor ultrassom HC-SR04
#define SR04_ECHO_PIN 35 // pino ECHO do sensor ultrassom HC-SR04
#define RELAY1_IN_PIN 33 // pino IN do relay para bomba d'agua

const int alturaReservatorio = 400; // altura do reservatorio de agua em cm

// inicializacao e configuracao da placa e pinos
void setup() {
  Serial.begin(115200);
  pinMode(SR04_TRIG_PIN, OUTPUT);
  pinMode(SR04_ECHO_PIN, INPUT);
  pinMode(RELAY1_IN_PIN, OUTPUT);
}

// loop principal
void loop() {
  controlarAgua(); // checar nivel de agua e ligar/desligar bomba d'agua
  delay(500); // Wait for 2 seconds before taking another reading
}

// usar sensor HC-SR04 e relé para medir nivel de agua e ligar/desligar bomba d'agua
void controlarAgua() {
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
  Serial.print("Nivel de agua: " + String(nivel) + "%\n");
  // controlar bomba de agua para manter reservatorio em torno de 80% cheio
  if (nivel < 80) {
    digitalWrite(RELAY1_IN_PIN, HIGH);
    Serial.println("Bomba de agua ligada.\n");
  } else if (nivel >= 80) {
    digitalWrite(RELAY1_IN_PIN, LOW);
    Serial.println("Bomba de agua desligada.\n");
  }
}
