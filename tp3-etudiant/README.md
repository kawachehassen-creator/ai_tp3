# TP 3 — De « Hello agent » à la boucle agentique

Code de départ du TP. Suivez la fiche « TP 3 » étape par étape.

## Installation (étape 0)

```bash
python -m venv .venv
# Linux/macOS : source .venv/bin/activate     Windows : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env        # Windows : copy .env.example .env
```

Ouvrez `.env`, collez votre clé, réglez `PROVIDER`.

## Fichiers

| Fichier | Étape |
| --- | --- |
| `config.py` | Choix du fournisseur et du modèle (lu dans `.env`) |
| `etape01a_hello_http.py` | 1 · appel HTTP brut, sans SDK |
| `etape01b_hello_sdk.py` | 1 · le même appel avec le SDK |
| `etape02_dissequer.py` | 2 · finish_reason, tokens (`python etape02_dissequer.py 20`) |
| `etape03_temperature.py` | 3 · température |
| `etape04_sans_etat.py` | 4 · l'expérience de l'oubli |
| `etape05_chatbot.py` | 5 · un chatbot avec historique |
| `etape06_qui_es_tu.py` | 6 · « Qui es-tu ? » (`python etape06_qui_es_tu.py groq qwen/qwen3.6-27b`) |
| `etape07_prompt_systeme.py` | 7 · le prompt système |
| `etape08_ne_peut_pas_agir.py` | 8 · le modèle ne peut pas agir |
| `outils.py` | Les outils de l'agent |
| `etape09_outil_fait_main.py` | 9 · un outil par convention de texte |
| `etape10_boucle_agentique.py` | 10 · la boucle agentique |
| `etape11_outils_natifs.py` | 11 · l'appel d'outils natif |
| `etape12_contexte_initial.py` | 12 · le contexte initial |

Règles : votre clé reste dans `.env` ; aucune donnée personnelle vers les API gratuites.
