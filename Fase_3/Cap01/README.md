# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Cap 1 - Construindo uma máquina agrícola

## One Man Band

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/jonatasgomes">Jônatas Gomes Alves</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Lucas Gomes Moreira</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi">André Godoi Chiovato</a>


## 📜 Descrição

*O objetivo do projeto na Fase 3 será desenvolver um sistema de irrigação automatizado e inteligente que monitore a umidade do solo em tempo real, os níveis dos nutrientes P e K representados por botões (que vão “medir” os níveis como tudo ou nada; “true” ou “false”; botão pressionado e não pressionado) e o nível de pH representado pelo sensor LDR (Light Dependent Resistor), ajustando a irrigação conforme o necessário, isto é, ligando uma bomba d’água representado por um relé.*

## 🤔 Funcionamento
Abaixo temos os 4 sensores ligados ao ESP32. Também incluso um relé para ligar/desligar irrigação conforme umidade lida. No terminal o sistema irá gerá como saída o JSON com os dados dos sensores. Esse JSON pode ser manualmente importado no sistema de monitoramento.
![Coleta de Dados - Sensores](assets/Wokwi_RM559693_FIAP_Cap1_01.jpg "Coleta de Dados - Sensores")

Aqui o código fonte usado no circuto acima.
![Coleta de Dados - Código Fonte](assets/Wokwi_RM559693_FIAP_Cap1_02.jpg "Coleta de Dados - Código Fonte")

Temos também a tela de monitoramento dos dados lidos pelos sensores. Desenvolvida em Python com Streamlit e Oracle.
![Sistema de Monitoramento - Dashboard](assets/Python_Monitoramento_01.jpg "Sistema de Monitoramento - Dashboard")

Vemos aqui a tela para input dos dados copiados dos sensores em formato JSON.
![Sistema de Monitoramento - Dados](assets/Python_Monitoramento_02.jpg "Sistema de Monitoramento - Dados")

Esse é o código fonte Python usado na interface com o banco de dados Oracle.
![Sistema de Monitoramento - Python e Oracle](assets/Python_Monitoramento_03.jpg "Sistema de Monitoramento - Python e Oracle")

## Link pro Vídeo
[Vídeo Demonstrando a Solução](https://youtu.be/7KczR_RljLA)

## 🗃 Histórico de lançamentos

* 1.0.0 - 11/11/2024

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

