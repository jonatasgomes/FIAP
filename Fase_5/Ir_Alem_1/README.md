# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Sistema de Coleta e Comunicação de Dados Usando ESP32 Integrado ao Wi-Fi

## Nome do grupo - Grupo 08

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/iolanda-helena-fabbrini-manzali-de-oliveira-14ab8ab0">Iolanda Helena Fabbrini Manzali de Oliveira</a>
- <a href="https://www.linkedin.com/company/inova-fusca">Murilo Carone Nasser</a> 
- <a href="https://www.linkedin.com/in/pedro-eduardo-soares-de-sousa-439552309">Pedro Eduardo Soares de Sousa</a> 
- <a href="https://www.linkedin.com/company/inova-fusca">Yago Brendon Iama</a>
- <a href="https://www.linkedin.com/in/jonatasgomes">Jônatas Gomes Alves</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/leonardoorabona">Leonardo Ruiz Orabona</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Andre Godoi Chaviato</a>

## 📜 Descrição

O projeto "Sistema de Coleta e Comunicação de Dados Usando ESP32 Integrado ao Wi-Fi" tem como objetivo desenvolver uma solução utilizando um ESP32 para coleta de dados via sensores e comunicação Wi-Fi. Os dados coletados são enviados diretamento a um banco de dados Oracle hospedado na Oracle Cloud. A comunicação é feita via api REST.

## 💻 Tecnologias utilizadas

#### Hardware
![microesp](https://github.com/user-attachments/assets/815e3951-ddec-4284-af49-368e83202b44)
  - **ESP32:** Microcontrolador wi-fi e Bluetooth, ideal para aplicações de IoT.
  - **DHT22:** sensor de temperatura e umidade
  - **LDR:** sensor de luz (resistor-dependente de luz) para medir a intensidade da luz
  - **Jumpers** e protoboard para conexões

#### Software
![ESP32](https://img.shields.io/badge/ESP32-000000?style=for-the-badge&logo=espressif&logoColor=white)
![MicroPython](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![JSON](https://img.shields.io/badge/json-5E5C5C?style=for-the-badge&logo=json&logoColor=white)
![REST API](https://img.shields.io/badge/REST-API-blue?style=for-the-badge)
![Oracle Cloud Database 23ai](https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white)
  - **WokWi:** Software online and gratuito para simulação de ESP32.
  - **MicroPython:** Linguagem de programação usada para escrever o código que fará as leituras dos dados dos sensores e mandará para o banco de dados.
  - **API REST:** Método de comunicação utilizado para enviar os dados para o banco Oracle.
  - **JSON:** Formato dos dados enviados ao banco Oracle.
  - **Oracle Cloud Database 23ai:** Banco de dados Oracle hospedado na nuvem.
  - **Oracle ORDS:** Ferramenta disponibilizada pela Oracle Cloud que permite criar e disponibiliar a **API REST**.
  - **Oracle SQL Developer** Ferramenta para acessar o banco de dados Oracle e visualizar/alterar os dados das tabelas.

## 📁 Estrutura de pastas

- **/docs** - Documentação do projeto
- **/src** - Código-fonte e scripts
- **/assets** - Imagens do circuito e diagrama de conexão
- **README.md** - Descrição do projeto

## 🔧 Como executar o Projeto
  1. Construir o projeto no WokWi, adicionando os componentes e carregando o código.
  2. Executar o código no WokWi e alterar os valores simulados dos sensores.
  3. Conectar a base de dados Oracle e verificar as linhas da tabela **SENSOR_LEITURAS**.
  4. Também é possível ler os dados gravados através da API REST.

## 🎥 Demonstração

Link para vídeo demonstrativo: [YouTube - Projeto Ir Além 1](#)

## 📋 Licença

Este projeto está licenciado sob a licença MIT. Para mais detalhes, consulte o arquivo LICENSE no repositório.

---

<p align="center">
<strong>Projeto desenvolvido para o curso de Inteligência Artificial da FIAP.</strong>
</p>
