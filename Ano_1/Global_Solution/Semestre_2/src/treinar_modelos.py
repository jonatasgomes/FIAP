import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression # Um pouco mais realista
import joblib
import os

# Criar pasta models se não existir
path = os.path.join(os.path.dirname(__file__), "modelos")
os.makedirs(path, exist_ok=True)

# Modelo Nível Esperado
# Suponha que treinamos com dados onde a média é 2.5m
X_dummy_expected = np.array([[1],[2],[3]]) # Features dummy (ex: dia do ano)
y_dummy_expected = np.array([2.4, 2.5, 2.6])
model_expected = LinearRegression() # Usando LinearRegression para exemplo
model_expected.fit(X_dummy_expected, y_dummy_expected) # Treinando com dados fictícios
joblib.dump(model_expected, path + "/modelo_nivel_esperado.joblib")
print("Modelo 'modelo_nivel_esperado.joblib' salvo.")

# Modelo Previsão Chuva
# Vamos assumir que ele prevê o *aumento* do nível devido à chuva.
X_dummy_rain = np.array([[10], [20], [50]]) # mm de chuva
y_dummy_rain_increase = np.array([0.1, 0.25, 0.7]) # aumento em metros
model_rain_prediction = LinearRegression()
model_rain_prediction.fit(X_dummy_rain, y_dummy_rain_increase)
joblib.dump(model_rain_prediction, path + "/modelo_previsao_chuva.joblib")
print("Modelo 'modelo_previsao_chuva.joblib' salvo.")
