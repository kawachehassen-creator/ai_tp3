"""
Étape 1b — Le même appel, avec le SDK « openai ».

Le SDK ne fait rien de magique : il construit la même requête HTTP que l'étape 1a,
l'envoie, et transforme le JSON reçu en objets Python (response.choices[0]...).
Il fonctionne avec Groq, Gemini, OpenRouter et Ollama car ils parlent le même format.
"""

from config import get_client

client, model = get_client()

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": "Bonjour ! Réponds en une seule phrase : que sais-tu faire ?"}
    ],
)

print(response.choices[0].message.content)
