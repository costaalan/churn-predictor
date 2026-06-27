# 📉 Churn Predictor — SaaS Customer Churn

Preditor de churn para SaaS usando Machine Learning (Random Forest).
Parte do portfólio de Alan Costa — AI Agent Developer.

## 🎯 Objetivo
Prever quais clientes têm maior probabilidade de cancelar, 
permitindo ações preventivas da equipe de Customer Success.

## 📊 Dados
- 1.000 clientes simulados (SaaS)
- Features: sessões, minutos ativos, erros, tickets, satisfação, plano, cidade
- 20.8% taxa de churn

## 🧠 Modelo
- Random Forest (scikit-learn)
- Acurácia: 93%+
- Top features: tickets, erros, minutos ativos

## 🚀 Uso

### Treinar
```bash
python generate_data.py
python train.py
```

### API de Predição
```bash
POST /api/churn/predict
Content-Type: application/json

{
  "sessoes": 2,
  "mins": 10,
  "erros": 5,
  "tickets": 4,
  "satisfacao": 2,
  "idade": 35
}
```

Resposta:
```json
{
  "churn_prob": 94.5,
  "nivel": "🔴 Alto",
  "predicao": 1
}
```

## 🛠️ Stack
- Python 3.13
- scikit-learn (Random Forest)
- SQLite
- Flask (API)
- joblib (serialização)

## 📁 Estrutura
```
churn-predictor/
├── generate_data.py   # Geração de dados simulados
├── train.py           # Treinamento do modelo
├── model.pkl          # Modelo treinado
├── churn.db           # SQLite com dados
├── api.py             # API Flask standalone
└── README.md
```

## 👤 Autor
Alan Costa — alancosta.dev
