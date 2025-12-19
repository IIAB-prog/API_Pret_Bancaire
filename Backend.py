# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
from flask import Flask, request, jsonify
import joblib
import pandas as pd



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
    data = request.get_json(force=True)  # récupérer JSON
    df = pd.DataFrame([data])            # transformer en DataFrame
    prediction = model.predict(df)[0]
    return jsonify({"Loan_Status": prediction})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render fournit le port dans $PORT
    app.run(host="0.0.0.0", port=port)

