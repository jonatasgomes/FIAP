# Instalar a biblioteca httr se não estiver instalada
if (!require(httr)) {
  install.packages("httr")
  library(httr)
}

# Definir a URL da API meteorológica pública
url_api <- "http://api.openweathermap.org/data/2.5/weather"

# Definir a chave de API (obtida gratuitamente no site da OpenWeatherMap)
chave_api <- "a029da6b23fdd979bd37e3813c854bb3"

# Obter a cidade e o país como argumentos de linha de comando
cidade <- commandArgs(trailingOnly = TRUE)[1]
pais <- commandArgs(trailingOnly = TRUE)[2]

# Codificar a cidade e o país para uso na URL
cidade_codificada <- URLencode(cidade)
pais_codificado <- tolower(pais)

# Montar a URL completa para a requisição
url_completa <- paste0(url_api, "?q=", cidade_codificada, ",", pais_codificado, "&APPID=", chave_api)

# Fazer a requisição GET para a API
resposta <- GET(url_completa)

# Verificar se a requisição foi bem-sucedida
if (status_code(resposta) == 200) {
  # Parsear o JSON de resposta
  dados_climaticos <- jsonlite::fromJSON(content(resposta, "text"))

  # Exibir as informações meteorológicas
  cat("Cidade: ", dados_climaticos$name, "\n")
  cat("País: ", dados_climaticos$sys$country, "\n")
  cat("Temperatura atual: ", dados_climaticos$main$temp - 273.15, "°C\n")
  cat("Umidade do ar: ", dados_climaticos$main$humidity, "%\n")
  cat("Condição climática: ", dados_climaticos$weather[[1]]["description"], "\n")
} else {
  cat("Erro ao obter os dados climáticos\n")
}
