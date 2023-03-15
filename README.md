# TP9 - Développez une application Web en utilisant Django
TP4 d'openClassRoom - Le but est de développer une application client suivant des spécifications techniques.
Ici l'application permet de:
- Créer un tournoi contenant 8 joueurs choisi par l'opérateur et s'affrontant sur N rondes contenant chacune 4 matchs.
- Valider la fin d'un round et saisir les résultats de chaque match.
- Stocker te tournoi dans sa globalité dans une table "tournament" tinyDB
- Créer des joueurs dans la table "players" tinyDB
- Consulter la liste des joueurs en base de données
- Consulter l'historique des tournois précedents avec une profondeur allant jusqu'aux matchs


## Installation

Utiliser [pip](https://pip.pypa.io/en/stable/) pour isntaller les dépendances.

```bash
git clone https://github.com/gmaOCR/TP4.git
pip install -r requirements.txt
python App.py

```
## Flake8
Pour générer un nouveau rapport de conformité PEP8 dans "flake-report"
```bash
flake8 --format=html --htmldir=flake-report
```
## License
[GNU](https://choosealicense.com/licenses/gpl-2.0/)