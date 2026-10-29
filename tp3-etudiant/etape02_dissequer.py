"""
Étape 2 — Disséquer la réponse.

On regarde TOUT ce que le modèle renvoie, pas seulement le texte :
  - choices[0].message.content : le texte généré
  - choices[0].finish_reason   : POURQUOI la génération s'est arrêtée
        "stop"       -> le modèle a produit son jeton de fin : il a « fini »
        "length"     -> on a atteint la limite max_tokens : réponse coupée
        "tool_calls" -> le modèle demande à appeler un outil (étape 11)
  - usage : combien de tokens sont entrés (prompt) et sortis (completion)
"""

import sys

from config import get_client

client, model = get_client()

# Changez cette valeur (ex. : python etape02_dissequer.py 20) pour voir l'effet de max_tokens
max_tokens = int(sys.argv[1]) if len(sys.argv) > 1 else 400

response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Explique en 5 phrases ce qu'est un réseau informatique."}],
    max_tokens=max_tokens,
)

print("=== Réponse complète (JSON) ===")
print(response.model_dump_json(indent=2, exclude_none=True))

choice = response.choices[0]
print("\n=== Ce qu'il faut retenir ===")
print(f"Modèle qui a répondu : {response.model}")
print(f"finish_reason        : {choice.finish_reason}")
print(f"Tokens en entrée     : {response.usage.prompt_tokens}")
print(f"Tokens en sortie     : {response.usage.completion_tokens}")
print(f"Total                : {response.usage.total_tokens}")
print(f"Texte                : {choice.message.content!r}")
