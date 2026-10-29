"""
Étape 4 — L'expérience de l'oubli.

Deux appels successifs. Dans le premier, on donne notre prénom.
Dans le second, on demande notre prénom. Le modèle va-t-il s'en souvenir ?
Prédisez la réponse AVANT de lancer le script.
"""

from config import get_client

client, model = get_client()

# Appel n°1
r1 = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Bonjour, je m'appelle Yasmine et j'étudie à Tunis."}],
)
print("Appel 1 ->", r1.choices[0].message.content)

# Appel n°2 : une nouvelle requête HTTP, indépendante de la première
r2 = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Comment je m'appelle, et où est-ce que j'étudie ?"}],
)
print("\nAppel 2 ->", r2.choices[0].message.content)
