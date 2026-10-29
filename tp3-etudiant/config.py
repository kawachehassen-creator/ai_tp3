"""
config.py — Un seul endroit pour choisir à quel modèle on parle.

Tous les fournisseurs utilisés dans ce TP parlent le même « dialecte » HTTP :
celui de l'API Chat Completions popularisée par OpenAI. Changer de fournisseur
revient donc à changer trois choses : l'adresse (base_url), la clé, le nom du modèle.

On lit ces réglages dans le fichier .env (jamais dans le code : une clé ne se
partage pas, ne se commit pas, ne se colle pas dans un chat).
"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # lit le fichier .env du dossier courant

PROVIDERS = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "key_env": "GROQ_API_KEY",
        "model": "openai/gpt-oss-20b",
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "key_env": "GEMINI_API_KEY",
        "model": "gemini-3.8-flash",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "model": None,  # à choisir parmi les modèles « :free » sur openrouter.ai/models
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "key_env": None,  # un modèle local n'a pas besoin de clé
        "model": "qwen2.5:1.5b",
    },
}


def provider_settings(provider=None):
    """Retourne un dict {provider, base_url, api_key, model} prêt à l'emploi."""
    provider = (provider or os.getenv("PROVIDER", "groq")).lower()
    if provider not in PROVIDERS:
        sys.exit(f"PROVIDER inconnu : {provider!r}. Choix possibles : {', '.join(PROVIDERS)}")

    p = PROVIDERS[provider]
    api_key = os.getenv(p["key_env"]) if p["key_env"] else "ollama"
    if not api_key:
        sys.exit(f"Clé manquante : ajoutez {p['key_env']}=... dans votre fichier .env")

    # MODEL dans .env permet de surcharger le modèle par défaut
    model = os.getenv("MODEL") or p["model"]
    if not model:
        sys.exit(f"Aucun modèle par défaut pour {provider} : ajoutez MODEL=... dans .env")

    base_url = os.getenv("BASE_URL") or p["base_url"]
    return {"provider": provider, "base_url": base_url, "api_key": api_key, "model": model}


def get_client(provider=None):
    """Retourne (client, nom_du_modele). Le client est un simple émetteur de requêtes HTTP."""
    s = provider_settings(provider)
    client = OpenAI(base_url=s["base_url"], api_key=s["api_key"])
    return client, s["model"]
