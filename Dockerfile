# Usa imagen oficial de Python
FROM python:3.11-slim

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (si necesitas alguna)
# RUN apt-get update && apt-get install -y libgomp1

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación y modelo
COPY app.py .
COPY modelo_XGBoost_estres.joblib modelo_XGBoost_estres.joblib

# Puerto expuesto (ajusta al puerto que usa tu API)
EXPOSE 5000

# Comando de inicio (ajusta según tu API)
CMD ["python", "app.py"]