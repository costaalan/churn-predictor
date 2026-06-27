"""API standalone do Churn Predictor"""
import joblib, json, os
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)
model = joblib.load(os.path.join(os.path.dirname(__file__), 'model.pkl'))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array([[
        float(data.get('idade',30)),
        float(data.get('sessoes',5)),
        float(data.get('mins',30)),
        int(data.get('erros',0)),
        int(data.get('tickets',0)),
        float(data.get('satisfacao',4)),
        float(data.get('plano_num',2)),
        float(data.get('cidade_num',1))
    ]])
    proba = model.predict_proba(features)[0]
    risco = round(proba[1] * 100, 1)
    nivel = '🟢 Baixo' if risco < 30 else ('🟡 Médio' if risco < 60 else '🔴 Alto')
    return jsonify({'churn_prob': risco, 'nivel': nivel, 'predicao': int(model.predict(features)[0])})

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
