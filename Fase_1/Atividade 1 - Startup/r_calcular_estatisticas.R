# Instale os pacotes necessários
if (!require('RSQLite')) install.packages('RSQLite')
if (!require('jsonlite')) install.packages('jsonlite')

# Carregar bibliotecas
library(RSQLite)
library(jsonlite)

# Conectar ao banco de dados SQLite
db_dir <- getwd()
con <- dbConnect(SQLite(), dbname = file.path(db_dir, "database.db"))

# Calcular estatísticas para a tabela 'areas'
query_areas <- "SELECT largura, comprimento, base, altura, raio, base_menor, area FROM areas"
dados_areas <- dbGetQuery(con, query_areas)
if (nrow(dados_areas) == 0) {
  dados_areas <- data.frame(largura = 0, comprimento = 0, base = 0, altura = 0, raio = 0, base_menor = 0, area = 0)
}

# Calcular estatísticas básicas
estatisticas_areas <- data.frame(
  variavel = c("largura", "comprimento", "base", "altura", "raio", "base_menor", "area"),
  media = round(
            c(mean(dados_areas$largura, na.rm = TRUE),
            mean(dados_areas$comprimento, na.rm = TRUE),
            mean(dados_areas$base, na.rm = TRUE),
            mean(dados_areas$altura, na.rm = TRUE),
            mean(dados_areas$raio, na.rm = TRUE),
            mean(dados_areas$base_menor, na.rm = TRUE),
            mean(dados_areas$area, na.rm = TRUE)),
            2
          ),
  desvio_padrao = round(
                    c(sd(dados_areas$largura, na.rm = TRUE),
                    sd(dados_areas$comprimento, na.rm = TRUE),
                    sd(dados_areas$base, na.rm = TRUE),
                    sd(dados_areas$altura, na.rm = TRUE),
                    sd(dados_areas$raio, na.rm = TRUE),
                    sd(dados_areas$base_menor, na.rm = TRUE),
                    sd(dados_areas$area, na.rm = TRUE)),
                    2
                  )
)
estatisticas_areas[is.na(estatisticas_areas)] <- 0

# Fechar a conexão
dbDisconnect(con)

# Exportar resultados como JSON
cat(toJSON(estatisticas_areas))
