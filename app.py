from flask import Flask, request, jsonify
from joblib import load
import numpy as np
import os

app = Flask(__name__)

# Cargar modelo preentrenado
modelo = load('modelo_XGBoost_estres.joblib')

@app.route('/predecir_estres', methods=['POST'])
def predecir_estres():
    try:
        datos = request.json
        
        umbral = float(datos.get('umbral', 0.6))
        
        caracteristicas_requeridas = [
            'headache', 
            'bullying', 
            'future_career_concerns', 
            'extracurricular_activities'
        ]
        
        for caracteristica in caracteristicas_requeridas:
            if caracteristica not in datos:
                return jsonify({
                    'error': f'Falta la característica: {caracteristica}'
                }), 400
        
        entrada = np.array([
            datos['headache'],
            datos['bullying'],
            datos['future_career_concerns'],
            datos['extracurricular_activities']
        ]).reshape(1, -1)
        
        probabilidades = modelo.predict_proba(entrada)
        
        proba_estres_alto = probabilidades[0][1]
        
        prediccion_binaria = 1 if proba_estres_alto > umbral else 0
        
        nivel_estres = "Alto" if prediccion_binaria == 1 else "Bajo"
        
        return jsonify({
            'prediccion_binaria': int(prediccion_binaria),
            'nivel_estres': nivel_estres,
            'probabilidad_estres_alto': float(proba_estres_alto),
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)