"""
Étape 10 — La boucle agentique.

À l'étape 9, on avait écrit à la main UN aller-retour. Mais une tâche peut demander
plusieurs outils, dans un ordre qu'on ne connaît pas à l'avance : c'est le modèle qui
décide. On remplace donc le « if » par un « while » :

    tant que le modèle demande une action (et qu'on n'a pas dépassé la limite) :
        exécuter l'action, renvoyer le résultat, redemander au modèle
    quand il « répond » : on s'arrête

C'est la boucle agentique : Penser -> Agir -> Observer -> recommencer.
"""

import json
import re

from config import get_client
from outils import OUTILS

client, model = get_client()

MAX_ITERATIONS = 6  # garde-fou : un agent ne doit jamais tourner sans fin

PROMPT_SYSTEME = """Tu es un agent qui résout des tâches étape par étape avec des outils.
Tu réponds TOUJOURS par un seul objet JSON, sans aucun autre texte :
{"pensee": "<ce que tu comptes faire et pourquoi>", "action": "<nom>", "argument": "<texte>"}

Actions disponibles :
- "heure_actuelle" : donne la date et l'heure actuelles. argument : "" (vide)
- "calculer" : évalue une expression arithmétique exacte. argument : ex. "(23 - 14) * 60 + 5"
- "repondre" : termine la tâche. argument : ta réponse finale pour l'utilisateur

Une seule action par réponse. Après chaque action, tu recevras un message OBSERVATION avec son résultat.
N'invente jamais un résultat : utilise un outil."""


def lire_json(texte):
    trouve = re.search(r"\{.*\}", texte, re.DOTALL)
    if not trouve:
        raise ValueError(f"Pas de JSON dans la réponse : {texte!r}")
    return json.loads(trouve.group(0))


def executer(action, argument):
    """Le harnais exécute l'action demandée et renvoie TOUJOURS du texte."""
    if action not in OUTILS:
        return f"ERREUR : l'action {action!r} n'existe pas. Actions possibles : {list(OUTILS)} ou repondre."
    fonction = OUTILS[action]
    try:
        return fonction(argument) if argument else fonction()
    except Exception as erreur:  # une erreur devient une observation, pas un plantage
        return f"ERREUR lors de l'exécution de {action} : {erreur}"


def agent(tache):
    messages = [
        {"role": "system", "content": PROMPT_SYSTEME},
        {"role": "user", "content": tache},
    ]
    for iteration in range(1, MAX_ITERATIONS + 1):
        response = client.chat.completions.create(model=model, messages=messages, temperature=0)
        texte = response.choices[0].message.content
        messages.append({"role": "assistant", "content": texte})

        try:
            decision = lire_json(texte)
        except (ValueError, json.JSONDecodeError) as erreur:
            # Le modèle n'a pas respecté le format : on le lui dit, et on continue la boucle
            messages.append({"role": "user", "content": f"OBSERVATION : format invalide ({erreur}). Réponds en JSON."})
            continue

        print(f"\n[tour {iteration}] pensée  : {decision.get('pensee', '')}")
        print(f"[tour {iteration}] action  : {decision.get('action')}({decision.get('argument', '')!r})")

        if decision.get("action") == "repondre":
            return decision.get("argument", "")

        observation = executer(decision.get("action"), decision.get("argument", ""))
        print(f"[tour {iteration}] observ. : {observation}")
        messages.append({"role": "user", "content": f"OBSERVATION : {observation}"})

    return "Arrêt : nombre maximal d'itérations atteint sans réponse finale."


if __name__ == "__main__":
    tache = "Quelle heure est-il, et combien de minutes reste-t-il avant minuit ?"
    print("Tâche :", tache)
    print("\nRéponse finale :", agent(tache))
