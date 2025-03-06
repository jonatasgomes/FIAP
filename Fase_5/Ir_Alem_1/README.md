# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto - A Eletrônica de uma IA
![wokwi](https://github.com/user-attachments/assets/9121d5b7-ec33-4f53-8622-e66fc293b60c)



## Nome do grupo - Grupo 08

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/hilmar-marques-358672161">Hilmar Gomes Marques da Silva</a>
- <a href="https://www.linkedin.com/in/iolanda-helena-fabbrini-manzali-de-oliveira-14ab8ab0">Iolanda Helena Fabbrini Manzali de Oliveira</a>
- <a href="https://www.linkedin.com/company/inova-fusca">Murilo Carone Nasser</a> 
- <a href="https://www.linkedin.com/in/pedro-eduardo-soares-de-sousa-439552309">Pedro Eduardo Soares de Sousa</a> 
- <a href="https://www.linkedin.com/company/inova-fusca">Yago Brendon Iama</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a">Lucas Gomes Moreira</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Andre Godoi Chaviato</a>

## 📜 Descrição

O projeto "A Eletônica de uma IA" proposta na terceira fase do Curso de Inteligência Artificial da FIAP tem como objetivo desenvolver um sistema inteligente de monitoramento agricola por sensores para coleta de dados ambientais, alem de detecção de movimentos, para em um cultivo de tomate.
O sistema  visa monitorar temperatura e umidade (sensor DHT22), nível de água (sensorHC-SR04), intensidade de luz (sensor LDR) e sensor de movimento PIR, otimizando a tomada de decisões no uso dos recursos, além de acrescentar uma camada de segurança, ao permitir a detecção de animais e/ou pessoas nas áreas cobertas pelo sensor.

## 💻Tecnologias utilizadas

![arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
![CPP](https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![JSON](https://img.shields.io/badge/json-5E5C5C?style=for-the-badge&logo=json&logoColor=white)


### Componentes do Modelo
![microesp](https://github.com/user-attachments/assets/815e3951-ddec-4284-af49-368e83202b44)

#### Hardware


	* ESP32: Microcontrolador wi-fi e Bluetooth, ideal para aplicações de IoT.
	 
	* DHT22: sensor de temperatura e umidade 
	
	* HC-SR04: sensor ultrasônico para medir o nível de água 

	* PIR: Sensor de movimento para detectar movimento na area monitorada 

	* LDR: sensor de luz (resistor-dependente de luz) para medir a intensidade da luz

  	* LCD I2C (16x2): Display para exibir as informaçoes do sistema

	* Jumpers e protoboard para conexões

#### Software

 	* Arduino IDE com suporte para ESP32

  	*Bibliotecas:
   		
     		** DHT (Adafruit)

     		** Ultrasonic

       		** LiquidCrystal_I2C


### Configuração do Projeto no Wokwi

O Wokwi é uma plataforma de simulação que permite rodar projetos com microcontroladores e sensores sem hardware físico. 

*Para simular o projeto:

	*Acesse wokwi.com

	* Crie um novo projeto ESP32.
	
 	* Copie e cole o código do projeto na área de código do Wokwi.
  
	* Adicione os componentes necessários no Wokwi:
 
		** DHT22, HC-SR04, PIR, LDR e LCD I2C
  
	* Conecte os componentes ao ESP32 conforme o esquema a seguir:
 
		# DHT22: Conectar ao pino GPIO16 do ESP32.
  
		# HC-SR04: Trigger ao pino GPIO4 e Echo ao pino GPIO5.
  
		# PIR: Conectar ao pino GPIO13.
  		
  		# LDR: Conectar ao pino GPIO12 (utilize um resistor pull-down para leituras estáveis).
  
		# LCD I2C: Conectar nos pinos I2C do ESP32 (GPIO21 - SDA e GPIO22 - SCL).
  
		# Clique em "Start Simulation" para iniciar a simulação do projeto.
  
    
## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: init
- <b>assets</b>: imagens em png do modelo ESP32

- <b>docs</b>: documentos FIAP Fase3

- <b>link</b>: link do projeto (url)
  
- <b>src</b>: código do projeto (.ino e .json)

- <b>test</b>: manual do usuário.

- <b>README.md</b>: init

  
## 🔧 Como executar o Projeto

 * Configurando o Ambiente

 	** Instale o Arduino IDE

 	** Adicione o suporte para ESP32 na IDE

 	** Instale as Bibliotecas necessárias através do Gerenciador de Bibliotecas 
  	
 
  * Conectando os sensores

 	** Conecte os sensores e o LCD ao ESP 32 conforme as instruções abaixo

    		DHT22: Pino 16

     		HC-SR04: Trigger no Pino 4 e Echo no Pino 5

    		PIR: Pino 13
    	  
		LDR: Pino 12 (ADC)

  		LCD I2C: Pinos I2C (GND, VCC, SDA, SCL)
    
		
 * Carregando o Código

  	**Copie o código fornecido para o arquivo de esboço da IDE do Arduino

 	** Conecte o ESP32 ao computador e selecione a porta correta
   
	** Faça o upload do código para o ESP32
   
	
 * Monitorando o sistema
   
	** Acesse o Monitor Serial da Arduino IDE para visualizar as leituras dos sensores

   	** Verifique o Display LCD para visualizar as informações em tempo real


   ![gifesp32](assets/esp32.gif)


## 🗃 Histórico de lançamentos

* 0.5.0 - XX/XX/2024
  
* 0.4.0 - XX/XX/2024

* 0.3.0 - XX/XX/2024
  
* 0.2.0 - XX/XX/2024   
  
* 0.1.0 - 05/11/2024
    

## 👨‍💻 Desenvolvedores

![grupo](assets/grupo.jpg)


## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

