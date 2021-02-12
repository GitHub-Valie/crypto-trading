Project is not maintained. Instead:

Visit https://github.com/GitHub-Valie/trading-app for the trading app (flask served react app)
Visit https://github.com/GitHub-Valie/trading-bot for the trading bot

# Projet : Algorithme de trading de cryptomonnaies

Ce projet vise à développer un algorithme capable de passer des ordres d'achat et de vente de cryptomonnaies sur la base d'une stratégie déterminée par l'utilisateur.
La stratégie repose sur des indicateurs d'analyse technique (moyennes mobiles, RSI) dont les paramètres sont ajustables.

## Le fonctionnement du projet:

### 1. Extraction des données
Avant même de commencer à acheter et vendre sur le marché, il faut l'observer. L'extraction des données historiques passées se fait grâce au logiciel de bases de données *MongoDB* et à la distribution *PyMongo*.
La visualisation des données peut être réalisée avec MatplotLib.

### 2. Backtesting, optimisation et paramétrage
Avant même de commencer à acheter et vendre sur le marché, il faut réfléchir à une stratégie de trading qui puisse être rentable. 
On a donc recours au *backtesting*, qui consiste à tester ses stratégies et à les optimiser sur des données passées, extraites en étape 1.
Pour ce projet, le backtesting est réalisé à l'aide de la librairie Python *Backtrader*.

### 3. Lancement du module main.py
Après avoir défini et optimisé la stratégie de trading, le programme main.py du dossier "bot" passera des ordres d'achat en toute autonomie.

### Par où commencer ?

Ces instructions vous aideront à obtenir une copie du projet qui soit fonctionnelle sur votre propre système. Il y a des prérequis pour que le programme fonctionne.

### Prérequis d'installation

1. Installations requises

* Installer Python version 3.5 ou une version plus récente 
https://www.python.org/downloads/

* Installer Visual Studio Code ou un autre environnement de développement
https://code.visualstudio.com/

* Installer Git
https://git-scm.com/

* Installer MongoDB Community
https://www.mongodb.com/try/download/community

2. Mise en route du projet

Après avoir installé les prérequis, il vous faudra :

* Clôner le dépôt github sur votre ordinateur
* Installer les modules grâce à la commande suivante dans votre IDE :

```
pip install -r requirements.txt
```

3. Créer un fichier config.py, utilisé pour la base de données et pour la connection à l'API Binance, ressemblant à ça :

Au préalable, il vous faudra créer un compte Binance si vous n'en possédez pas encore un.

```
mongodb = {
    "host": "hote mongo",
    "user": "utilisateur mongo",
    "passwd": "mot de passe mongo",
    "db": "binance",
}

binance = {
    "user": "un nom pour stocker en base",
    "public_key": "clé publique binance",
    "secret_key": "clé secrète binance"
}

```

