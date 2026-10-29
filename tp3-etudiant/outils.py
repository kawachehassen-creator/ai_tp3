"""
outils.py — Les « mains » de notre agent.

Un outil est une fonction Python ORDINAIRE. Le modèle ne l'exécute jamais lui-même :
il écrit une DEMANDE (du texte), et c'est notre programme qui exécute la fonction,
puis renvoie le résultat au modèle sous forme de texte.

Chaque outil prend des chaînes de caractères et renvoie une chaîne de caractères,
car le modèle ne lit et n'écrit que du texte.
"""

import ast
import operator
from datetime import datetime

# --- Outil 1 : une calculatrice sûre -------------------------------------------
# On n'utilise PAS eval() : une expression envoyée par le modèle pourrait contenir
# du code dangereux. On analyse l'expression et on n'autorise que l'arithmétique.

_OPERATIONS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _evaluer(noeud):
    if isinstance(noeud, ast.Constant) and isinstance(noeud.value, (int, float)):
        return noeud.value
    if isinstance(noeud, ast.BinOp) and type(noeud.op) in _OPERATIONS:
        return _OPERATIONS[type(noeud.op)](_evaluer(noeud.left), _evaluer(noeud.right))
    if isinstance(noeud, ast.UnaryOp) and type(noeud.op) in _OPERATIONS:
        return _OPERATIONS[type(noeud.op)](_evaluer(noeud.operand))
    raise ValueError("expression non autorisée")


def calculer(expression: str) -> str:
    """Évalue une expression arithmétique, ex. '48763 * 9241' ou '(24 - 13) * 60'."""
    try:
        expression = expression.replace("×", "*").replace("÷", "/")
        resultat = _evaluer(ast.parse(expression, mode="eval").body)
        return str(resultat)
    except Exception as erreur:  # on renvoie l'erreur AU MODÈLE, en texte
        return f"ERREUR : impossible de calculer {expression!r} ({erreur})"


# --- Outil 2 : l'horloge --------------------------------------------------------

def heure_actuelle() -> str:
    """Renvoie la date et l'heure locales, ex. 'mardi 27/10/2026 14:05'."""
    jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    maintenant = datetime.now()
    return f"{jours[maintenant.weekday()]} {maintenant.strftime('%d/%m/%Y %H:%M')}"


# Le registre : nom de l'outil (tel que le modèle l'écrira) -> fonction Python
OUTILS = {
    "calculer": calculer,
    "heure_actuelle": heure_actuelle,
}
