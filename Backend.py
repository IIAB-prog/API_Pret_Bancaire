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


import requests
import base64
from datetime import datetime
import os

@app.route('/comment', methods=['POST'])
def save_comment():
    data = request.get_json(force=True)

    commentaire = data.get("commentaire", "")
    note = data.get("note", "")

    if not commentaire:
        return jsonify({"error": "Commentaire vide"}), 400

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    path = "avis.json"

    api_url = f"https://api.github.com/repos/{repo}/contents/{path}"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Récupérer le fichier existant
    r = requests.get(api_url, headers=headers)

    if r.status_code == 200:
        content = r.json()
        sha = content["sha"]
        existing_data = json.loads(
            base64.b64decode(content["content"]).decode("utf-8")
        )
    else:
        sha = None
        existing_data = []

    # Ajouter le commentaire
    existing_data.append({
        "commentaire": commentaire,
        "note": note,
        "date": datetime.utcnow().isoformat()
    })

    encoded_content = base64.b64encode(
        json.dumps(existing_data, indent=4).encode("utf-8")
    ).decode("utf-8")

    payload = {
        "message": "Ajout d’un avis utilisateur",
        "content": encoded_content
    }

    if sha:
        payload["sha"] = sha

    put_response = requests.put(api_url, headers=headers, json=payload)

    if put_response.status_code in [200, 201]:
        return jsonify({"status": "Commentaire enregistré"})
    else:
        return jsonify({"error": "Échec de l’enregistrement"}), 500



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

