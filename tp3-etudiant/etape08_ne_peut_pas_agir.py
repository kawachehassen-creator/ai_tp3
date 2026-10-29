"""
Étape 8 — Constater : le modèle ne peut pas agir.

Un modèle ne fait qu'une chose : produire du texte à partir du texte reçu.
Il n'a ni horloge, ni calculatrice, ni accès à votre disque.
On lui pose trois questions qui demandent d'AGIR sur le monde, et on compare
avec la vérité calculée par Python.
"""

import os
from datetime import datetime

from config import get_client

client, model = get_client()


def demander(question):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


print("1) Quelle heure est-il ?")
print("   Modèle :", demander("Quelle heure est-il exactement ? Réponds par l'heure seule."))
print("   Vérité :", datetime.now().strftime("%H:%M"))

print("\n2) Un calcul exact")
print("   Modèle :", demander("Combien font 48763 × 9241 ? Réponds par le nombre seul, sans calculer étape par étape."))
print("   Vérité :", 48763 * 9241)

print("\n3) Le contenu de mon dossier")
print("   Modèle :", demander("Quels fichiers se trouvent dans mon dossier courant ? Liste-les."))
print("   Vérité :", sorted(os.listdir(".")))
