"""
Étape 1a — « Hello agent » sans aucune bibliothèque d'IA.

Objectif : voir qu'un appel à un modèle n'est RIEN D'AUTRE qu'une requête HTTP
POST contenant du JSON, et une réponse HTTP contenant du JSON.
On n'utilise que la bibliothèque standard de Python (urllib + json).
"""

import json
import urllib.error
import urllib.request

from config import provider_settings

s = provider_settings()

# 1. L'adresse : base_url + le chemin de l'API « chat completions »
url = s["base_url"].rstrip("/") + "/chat/completions"

# 2. Le corps de la requête : quel modèle, et quels messages
body = {
    "model": s["model"],
    "messages": [
        {"role": "user", "content": "Bonjour ! Réponds en une seule phrase : que sais-tu faire ?"}
    ],
}

# 3. Les en-têtes : le format du corps, et la preuve qu'on a le droit d'appeler (la clé)
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {s['api_key']}",
}

request = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers)

print(f"POST {url}")
print("Corps envoyé :")
print(json.dumps(body, indent=2, ensure_ascii=False))

try:
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    # Une erreur HTTP a aussi un corps JSON : il explique le problème (clé, quota, modèle...)
    print(f"\nErreur HTTP {e.code}")
    print(e.read().decode("utf-8"))
    raise SystemExit(1)

print("\nRéponse brute reçue :")
print(json.dumps(data, indent=2, ensure_ascii=False))

print("\nLe texte produit par le modèle :")
print(data["choices"][0]["message"]["content"])
