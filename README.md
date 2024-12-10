# Scraping Tool for PCGamingWiki

## Description

Ce projet est un outil de scraping écrit en Python qui permet de récupérer des informations sur les chemins de sauvegarde de jeux vidéo depuis le site [PCGamingWiki](https://www.pcgamingwiki.com). Il utilise des bibliothèques comme `BeautifulSoup`, `Playwright`, et `asyncio` pour naviguer, extraire et sauvegarder les données de manière asynchrone.

## Fonctionnalités

- Extraction des chemins de sauvegarde des jeux vidéo depuis PCGamingWiki.
- Utilisation de Playwright pour la navigation rapide et asynchrone des pages web.
- Sauvegarde des informations extraites dans des fichiers texte pour chaque jeu.
- Interface utilisateur simple avec saisie d'URL pour spécifier le jeu.

## Prérequis

Avant de commencer, vous devez avoir les outils suivants installés :

- [Python 3.7+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/), pour installer les packages Python
- [Node.js](https://nodejs.org/), nécessaire pour exécuter Playwright

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/Unk404j/scrapping-tool.git
    cd scrapping-tool
    ```

2. Installez les dépendances Python :
    ```bash
    pip install -r requirements.txt
    ```

3. Installez Playwright :
    ```bash
    playwright install
    ```

## Utilisation

1. Exécutez le script Python `main.py` pour démarrer le processus de scraping :
    ```bash
    python main.py
    ```

2. Lors de l'exécution, le programme vous demandera de saisir l'URL d'un jeu sur PCGamingWiki.

3. Le script extraiera les chemins de sauvegarde disponibles pour ce jeu et les enregistrera dans un fichier texte portant le nom de l'URL du jeu.

4. Le fichier `.txt` sera créé dans le même répertoire où vous avez exécuté le script.

## Contribuer

Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet ou ajouter des fonctionnalités, voici comment procéder :

1. Forkez le projet.
2. Créez une nouvelle branche pour votre fonctionnalité :
    ```bash
    git checkout -b ma-nouvelle-fonctionnalité
    ```
3. Commitez vos modifications :
    ```bash
    git commit -am 'Ajout de ma nouvelle fonctionnalité'
    ```
4. Poussez vos modifications sur votre fork :
    ```bash
    git push origin ma-nouvelle-fonctionnalité
    ```
5. Ouvrez une pull request sur le dépôt original pour que nous puissions réviser vos modifications.

## Auteurs

- **Unk404j** - _Développeur principal_ - [Unk404j GitHub](https://github.com/Unk404j)

## License

Ce projet est sous **Licence MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

MIT License

Copyright (c) 2024 Unk404j

Permission est accordée, gratuitement, à toute personne obtenant une copie de ce logiciel et des fichiers associés, de traiter dans le logiciel sans restriction, y compris les droits de l'utiliser, de le copier, de le modifier, de le fusionner, de le publier, de le distribuer, de le sous-licencier et/ou de le vendre, sous réserve des conditions suivantes :

L'avis de droit d'auteur ci-dessus et cet avis de permission doivent être inclus dans toutes les copies ou parties substantielles du logiciel.

LE LOGICIEL EST FOURNI "EN L'ÉTAT", SANS GARANTIE D'AUCUNE SORTE, EXPRESSE OU IMPLICITE, Y COMPRIS MAIS SANS S'Y LIMITER AUX GARANTIES DE QUALITÉ MARCHANDE, D'ADAPTATION À UN USAGE PARTICULIER ET DE NON-VIOLATION. EN AUCUN CAS LES AUTEURS OU DÉTENTEURS DU DROIT D'AUTEUR NE SERONT RESPONSABLES DE TOUTE RÉCLAMATION, DOMMAGE OU AUTRE RESPONSABILITÉ, QUE CE SOIT DANS UNE ACTION CONTRACTUELLE, DÉLICTUELLE OU AUTRE, DÉCOULANT DE, OUTRE OU EN RELATION AVEC LE LOGICIEL OU L'UTILISATION OU D'AUTRES ACTIONS DANS LE LOGICIEL.

