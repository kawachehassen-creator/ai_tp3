"""
Étape 3 — Le modèle est probabiliste.

À chaque pas, le modèle produit une distribution de probabilités sur le prochain token,
puis on TIRE un token dans cette distribution. La température règle ce tirage :
  - température basse (0)  -> on prend presque toujours le token le plus probable
  - température haute (1+) -> on laisse leur chance aux tokens moins probables
On pose 5 fois la même question avec deux températures et on compare.
"""

from config import get_client

client, model = get_client()

QUESTION = "Invente un nom pour une startup tunisienne de livraison. Réponds par le nom seul."

for temperature in (0.0, 1.2):
    print(f"\n--- température = {temperature} ---")
    for i in range(5):
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": QUESTION}],
            temperature=temperature,
        )
        print(f"{i + 1}. {response.choices[0].message.content.strip()}")
