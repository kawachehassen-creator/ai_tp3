"""
Étape 6 — Expérience : « Qui es-tu ? »

Nous posons trois questions SANS prompt système (seulement un message user) :
  Q1. Qui es-tu, et qui t'a créé ?
  Q2. Quelle est la date d'aujourd'hui ?
  Q3. Jusqu'à quelle date vont tes connaissances ?

Lancez le script sur au moins deux fournisseurs/modèles et remplissez le tableau
de la fiche de TP. Exemples :
    python etape06_qui_es_tu.py                 (fournisseur du .env)
    python etape06_qui_es_tu.py gemini
    python etape06_qui_es_tu.py groq qwen/qwen3.6-27b
Puis posez les MÊMES questions dans l'application web (chatgpt.com, gemini.google.com,
claude.ai...) et comparez.
"""

import sys

from config import get_client

QUESTIONS = [
    "Qui es-tu, et qui t'a créé ? Réponds en deux phrases.",
    "Quelle est la date d'aujourd'hui ? Réponds en une phrase.",
    "Jusqu'à quelle date vont tes connaissances ? Réponds en une phrase.",
]

provider = sys.argv[1] if len(sys.argv) > 1 else None
client, model = get_client(provider)
if len(sys.argv) > 2:
    model = sys.argv[2]

print(f"Modèle interrogé : {model}\n")
for i, question in enumerate(QUESTIONS, start=1):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],  # aucun message "system" !
        temperature=0,
    )
    print(f"Q{i}. {question}")
    print(f"R{i}. {response.choices[0].message.content.strip()}")
    print(f"     (tokens en entrée : {response.usage.prompt_tokens})\n")
