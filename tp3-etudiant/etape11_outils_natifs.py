"""
Étape 11 — La même boucle, avec l'appel d'outils NATIF de l'API.

À l'étape 10, NOUS avons inventé le protocole (du JSON décrit dans le prompt système)
et NOUS l'analysions avec une expression régulière. Les fournisseurs ont standardisé
exactement cette idée :
  - on décrit les outils dans le paramètre `tools` (nom, description, paramètres en JSON Schema) ;
  - le modèle (entraîné pour ça) répond avec `tool_calls` au lieu de texte ;
  - on renvoie chaque résultat dans un message de rôle "tool", lié par `tool_call_id`.
Le principe ne change pas : le modèle DEMANDE, le harnais EXÉCUTE, le modèle OBSERVE.
"""

import json

from config import get_client
from outils import OUTILS

client, model = get_client()

MAX_ITERATIONS = 6

# La description des outils, au format standard (JSON Schema)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "heure_actuelle",
            "description": "Donne la date et l'heure locales actuelles.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculer",
            "description": "Évalue exactement une expression arithmétique (+ - * / // % **, parenthèses).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "ex. '(23 - 14) * 60 + 5'"}
                },
                "required": ["expression"],
            },
        },
    },
]


def message_assistant(message):
    """Recopie la demande du modèle (son texte + ses tool_calls) pour la renvoyer au tour suivant.
    On copie chaque tool_call tel quel : certains fournisseurs y glissent des champs
    supplémentaires qu'ils exigent de retrouver au tour suivant."""
    m = {"role": "assistant", "content": message.content or ""}
    if message.tool_calls:
        m["tool_calls"] = [appel.model_dump(exclude_none=True) for appel in message.tool_calls]
    return m


def agent(tache):
    messages = [
        {"role": "system", "content": "Tu es un agent précis. Utilise les outils pour toute information "
                                      "ou tout calcul que tu ne peux pas connaître avec certitude."},
        {"role": "user", "content": tache},
    ]
    for iteration in range(1, MAX_ITERATIONS + 1):
        response = client.chat.completions.create(model=model, messages=messages, tools=TOOLS)
        message = response.choices[0].message
        print(f"\n[tour {iteration}] finish_reason = {response.choices[0].finish_reason}")

        # On ajoute la demande du modèle à l'historique (sinon il ne saurait plus ce qu'il a demandé)
        messages.append(message_assistant(message))

        if not message.tool_calls:  # pas de demande d'outil : c'est la réponse finale
            return message.content

        for appel in message.tool_calls:
            nom = appel.function.name
            arguments = json.loads(appel.function.arguments or "{}")  # les arguments arrivent en TEXTE JSON
            print(f"[tour {iteration}] le modèle demande : {nom}({arguments})")

            if nom not in OUTILS:
                resultat = f"ERREUR : outil inconnu {nom!r}"
            else:
                try:
                    resultat = OUTILS[nom](**arguments)
                except Exception as erreur:  # une erreur devient une observation, pas un plantage
                    resultat = f"ERREUR lors de l'exécution de {nom} : {erreur}"
            print(f"[tour {iteration}] résultat          : {resultat}")

            messages.append({"role": "tool", "tool_call_id": appel.id, "content": resultat})

    return "Arrêt : nombre maximal d'itérations atteint sans réponse finale."


if __name__ == "__main__":
    tache = "Quelle heure est-il, et combien de minutes reste-t-il avant minuit ?"
    print("Tâche :", tache)
    print("\nRéponse finale :", agent(tache))
