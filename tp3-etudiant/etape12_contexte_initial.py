"""
Étape 12 — Construire le contexte initial.

Le modèle ne connaît du monde QUE ce qui est dans son contexte (les messages envoyés).
Avant même le premier tour de boucle, le harnais doit donc ASSEMBLER ce contexte :
  1. l'identité et le rôle de l'agent ;
  2. ses règles de conduite ;
  3. l'environnement (date, fuseau, système, dossier de travail) ;
  4. ce qu'on sait de l'utilisateur ;
  5. la tâche.
Les outils, eux, sont décrits dans le paramètre `tools` (étape 11) : ils font aussi
partie du contexte, car le fournisseur les insère dans le texte que lit le modèle.

Partie A : on compare la même question AVEC et SANS la section « environnement ».
Partie B : on lance l'agent de l'étape 11 avec un contexte initial complet.
"""

import json
import os
import platform
from datetime import datetime

from config import get_client
from etape11_outils_natifs import TOOLS, message_assistant
from outils import OUTILS

client, model = get_client()

UTILISATEUR = {"prenom": "Yasmine", "niveau": "3e année LSI", "langue": "français"}


def section_identite():
    return "# Identité\nTu es « Atlas », l'assistant de travail d'un(e) étudiant(e) en informatique."


def section_regles():
    return ("# Règles\n"
            "- Réponds en français, de façon concise.\n"
            "- Pour tout calcul ou toute information que tu ne peux pas connaître, utilise un outil.\n"
            "- Si une information manque, dis-le au lieu d'inventer.")


def section_environnement():
    maintenant = datetime.now().astimezone()
    jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    jour = jours[maintenant.weekday()]
    return ("# Environnement\n"
            f"- Date et heure actuelles : {jour} {maintenant.strftime('%d/%m/%Y %H:%M')} (UTC{maintenant.strftime('%z')})\n"
            f"- Système d'exploitation : {platform.system()} {platform.release()}\n"
            f"- Dossier de travail : {os.getcwd()}")


def section_utilisateur(u):
    return f"# Utilisateur\n- Prénom : {u['prenom']}\n- Niveau : {u['niveau']}\n- Langue préférée : {u['langue']}"


def construire_contexte_initial(tache, avec_environnement=True):
    sections = [section_identite(), section_regles()]
    if avec_environnement:
        sections.append(section_environnement())
    sections.append(section_utilisateur(UTILISATEUR))
    prompt_systeme = "\n\n".join(sections)
    return [
        {"role": "system", "content": prompt_systeme},
        {"role": "user", "content": tache},
    ]


def partie_a():
    question = "Quel jour de la semaine serons-nous dans 10 jours ? Réponds en une phrase."
    for avec_env in (False, True):
        messages = construire_contexte_initial(question, avec_environnement=avec_env)
        r = client.chat.completions.create(model=model, messages=messages, temperature=0)
        print(f"\n--- avec environnement = {avec_env} ---")
        print(f"Réponse          : {r.choices[0].message.content.strip()}")
        print(f"Tokens en entrée : {r.usage.prompt_tokens}")


def partie_b():
    tache = "Combien de minutes reste-t-il avant minuit ? Appelle-moi par mon prénom."
    messages = construire_contexte_initial(tache)

    print("\n=== Le contexte initial, tel que le modèle va le recevoir ===")
    print(messages[0]["content"])
    print(f"\n[user] {tache}")
    print(f"[outils] {[t['function']['name'] for t in TOOLS]}")
    taille = len(json.dumps(messages, ensure_ascii=False)) + len(json.dumps(TOOLS, ensure_ascii=False))
    print(f"\nTaille approximative : {taille} caractères ≈ {taille // 4} tokens (règle approximative : 1 token ≈ 4 caractères)")

    for iteration in range(1, 7):
        response = client.chat.completions.create(model=model, messages=messages, tools=TOOLS)
        message = response.choices[0].message
        if iteration == 1:
            print(f"Tokens réellement comptés par le fournisseur au 1er appel : {response.usage.prompt_tokens}")
        messages.append(message_assistant(message))
        if not message.tool_calls:
            print("\nRéponse finale :", message.content)
            return
        for appel in message.tool_calls:
            arguments = json.loads(appel.function.arguments or "{}")
            resultat = OUTILS[appel.function.name](**arguments) if appel.function.name in OUTILS else "ERREUR : outil inconnu"
            print(f"[tour {iteration}] {appel.function.name}({arguments}) -> {resultat}")
            messages.append({"role": "tool", "tool_call_id": appel.id, "content": resultat})
    print("Arrêt : limite d'itérations atteinte.")


if __name__ == "__main__":
    partie_a()
    partie_b()
