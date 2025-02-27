##### FIAP /Fase 5 /Ir Além  /Opção 1  /Sistema de Coleta e Comunicação de Dados Usando ESP32 Integrado ao Wi-Fi

# Guia de Uso da API REST

## Endpoints

### 1. Obter todos os registros
- **URL:** `https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras`
- **Método:** `GET`
- **Descrição:** Retorna uma lista de todos os registros disponíveis.
- **Exemplo de Requisição via CURL:**
  ```bash
  curl -L -X GET "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras" -H "Accept: application/json"
  ```
- **Exemplo de Requisição via Browser:**
  ```
  https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras
  ```

### 2. Obter um registro específico
- **URL:** `https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras/{id}`
- **Método:** `GET`
- **Parâmetros:**
  - `id` (inteiro) - O identificador do registro desejado.
- **Descrição:** Retorna os detalhes de um único registro com base no ID fornecido.
- **Exemplo de Requisição via CURL:**
  ```bash
  curl -L -X GET "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras/1" -H "Accept: application/json"
  ```
- **Exemplo de Requisição via Browser:**
  ```
  https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras/1
  ```

### 3. Criar um novo registro
- **URL:** `https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras`
- **Método:** `POST`
- **Descrição:** Cria um novo registro usando os dados fornecidos no corpo da requisição em formato JSON.
- **Headers:**
  - `Content-Type: application/json`
- **Corpo da Requisição (JSON):**
  ```json
  {
    "data_leitura": "2025-02-27T13:16:36.333Z",
    "sensor": "string",
    "valor": 120
  }
  ```
- **Exemplo de Requisição via CURL:**
  ```bash
  curl -L -X POST "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras" \
       -H "Content-Type: application/json" \
       -d '{
            "data_leitura": "2025-02-27T13:16:36.333Z",
            "sensor": "UMIDADE",
            "valor": 120
          }'
  ```

## Observações
- Os itens 1 e 2 (método GET) podem ser executados diretamente do browser.
- Para garantir respostas em JSON, inclua o header `Accept: application/json`.
- O campo `id` é gerado automaticamente para cada novo registro.
- Autenticação: por simplicidade o serviço não requer autenticação.
