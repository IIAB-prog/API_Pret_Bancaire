# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

# Charger le modèle
model = joblib.load("eligibilite_pret_model.pkl")

# Initialiser Flask
app = Flask(__name__)

# Route principale
@app.route('/')
def home():
    return "API Loan Eligibility est en ligne !"

# Route de prédiction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    df = pd.DataFrame([data])

    # Prédiction (Y / N)
    prediction = model.predict(df)[0]

    # Probabilité (classe positive = Y)
    probability = model.predict_proba(df)[0][1]

    return jsonify({
        "Loan_Status": prediction,
        "Probability": round(float(probability), 4)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
