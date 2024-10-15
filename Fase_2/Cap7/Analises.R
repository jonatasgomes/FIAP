#JonatasGomesAlves_RM559693

# 3. analise exploratoria na variavel Valor
install.packages("readxl")
library(readxl)
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
data <- read_excel("Dados_Agronegocio.xlsx")
valor <- data$'Valor ($)'

# 3.1. Medidas de Tendência Central
media <- mean(valor)
mediana <- median(valor)
moda <- as.numeric(names(sort(-table(valor)))[1])  # Moda

# 3.2. Medidas de Dispersão
variancia <- var(valor)
desvio_padrao <- sd(valor)
amplitude <- max(valor) - min(valor)

# 3.3. Medidas Separatrizes
quartis <- quantile(valor)
percentis <- quantile(valor, probs = c(0.1, 0.25, 0.5, 0.75, 0.9))

# 3.4. Análise Gráfica
par(mfrow = c(1, 2))  # Configura layout com 2 gráficos

# Histograma
hist(valor, main = "Histograma de Valor ($)", xlab = "Valor ($)", col = "lightblue", border = "black")

# Boxplot
boxplot(valor, main = "Boxplot de Valor ($)", ylab = "Valor ($)", col = "lightgreen")

# Mostrar os resultados
list(
  Media = media,
  Mediana = mediana,
  Moda = moda,
  Variancia = variancia,
  Desvio_Padrao = desvio_padrao,
  Amplitude = amplitude,
  Quartis = quartis,
  Percentis = percentis
)

# 4. análise gráfica na variavel Tipo de Cultivo
install.packages("ggplot2")
library(ggplot2)
table(data$'Tipo de Cultivo')
ggplot(data, aes(x = 'Tipo de Cultivo')) +
  geom_bar(fill = "skyblue", color = "black") +
  theme_minimal() +
  labs(title = "Distribuição dos Tipos de Cultivo", x = "Tipo de Cultivo", y = "Frequência")
