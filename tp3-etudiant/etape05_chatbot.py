"""
Étape 5 — Construire un chatbot : la « mémoire » est une liste Python.

Le modèle ne se souvient de rien (étape 4). Pour qu'il « se souvienne », c'est NOTRE
programme (le harnais) qui garde l'historique et le RENVOIE EN ENTIER à chaque appel.

Commandes : /quit pour sortir, /historique pour voir ce qui est envoyé au modèle.
Observez la colonne « tokens en entrée » : elle grandit à chaque tour. Pourquoi ?
"""

import json

from config import get_client

client, model = get_client()

historique = []  # la seule « mémoire » de notre chatbot

print(f"Chatbot prêt (modèle : {model}). Tapez /quit pour sortir.\n")

while True:
    texte = input("Vous > ").strip()
    if not texte:
        continue
    if texte == "/quit":
        break
    if texte == "/historique":
        print(json.dumps(historique, indent=2, ensure_ascii=False))
        continue

    # 1. On ajoute le message de l'utilisateur à l'historique
    historique.append({"role": "user", "content": texte})

    # 2. On envoie TOUT l'historique au modèle
    response = client.chat.completions.create(model=model, messages=historique)
    reponse = response.choices[0].message.content

    # 3. On ajoute la réponse du modèle à l'historique (sinon il oubliera ce qu'il a dit)
    historique.append({"role": "assistant", "content": reponse})

    print(f"IA   > {reponse}")
    print(f"       [messages envoyés : {len(historique) - 1} | "
          f"tokens en entrée : {response.usage.prompt_tokens} | "
          f"tokens en sortie : {response.usage.completion_tokens}]\n")
