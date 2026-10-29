"""
Étape 9 — Un outil « fait main » : une simple convention de texte.

Le modèle ne sait produire que du texte. Pour qu'il « utilise » une calculatrice :
  1. on lui EXPLIQUE (prompt système) un format de réponse : du JSON avec une action ;
  2. notre programme LIT ce texte, reconnaît la demande, exécute la fonction Python ;
  3. on RENVOIE le résultat au modèle dans un nouveau message ;
  4. le modèle, qui voit maintenant le résultat, rédige la réponse finale.
Ici, un seul aller-retour. La boucle viendra à l'étape 10.
"""

import json
import re

from config import get_client
from outils import calculer

client, model = get_client()

PROMPT_SYSTEME = """Tu disposes d'une calculatrice exacte. Tu réponds TOUJOURS par un seul objet JSON, sans aucun autre texte.
Deux formats possibles :
{"action": "calculer", "argument": "<expression arithmétique, ex. 12 * (3 + 4)>"}
{"action": "repondre", "argument": "<ta réponse finale pour l'utilisateur>"}
Pour tout calcul, utilise d'abord "calculer". Quand tu reçois un message qui commence par RÉSULTAT, utilise-le pour "repondre"."""


def lire_json(texte):
    """Extrait le premier objet {...} du texte du modèle (il ajoute parfois des ```)."""
    trouve = re.search(r"\{.*\}", texte, re.DOTALL)
    if not trouve:
        raise ValueError(f"Pas de JSON dans la réponse : {texte!r}")
    return json.loads(trouve.group(0))


messages = [
    {"role": "system", "content": PROMPT_SYSTEME},
    {"role": "user", "content": "Combien font 48763 × 9241 ?"},
]

# --- Appel 1 : le modèle doit DEMANDER le calcul ---
texte = client.chat.completions.create(model=model, messages=messages, temperature=0).choices[0].message.content
print("Modèle (appel 1) :", texte)
demande = lire_json(texte)

if demande["action"] == "calculer":
    # --- Notre programme exécute l'outil : c'est ici que l'action a lieu ---
    resultat = calculer(demande["argument"])
    print(f"Harnais : j'exécute calculer({demande['argument']!r}) -> {resultat}")

    # --- On renvoie au modèle ce qu'il a dit ET le résultat ---
    messages.append({"role": "assistant", "content": texte})
    messages.append({"role": "user", "content": f"RÉSULTAT de calculer : {resultat}"})

    # --- Appel 2 : le modèle rédige la réponse finale ---
    texte = client.chat.completions.create(model=model, messages=messages, temperature=0).choices[0].message.content
    print("Modèle (appel 2) :", texte)
    demande = lire_json(texte)

print("\nRéponse finale :", demande["argument"])
