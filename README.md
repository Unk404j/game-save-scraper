# Scraper PCGamingWiki

Ce script permet de récupérer les chemins de sauvegarde des jeux vidéo présents sur le site **PCGamingWiki**. Il utilise **Playwright** pour naviguer de manière asynchrone dans un navigateur web et **BeautifulSoup** pour analyser et extraire les données de la page.

## Prérequis

- Python 3.7 ou supérieur.
- Bibliothèques Python suivantes :
  - `playwright`
  - `beautifulsoup4`
  - `html5lib`
  - `re`

Tu peux installer les dépendances nécessaires via `pip` en exécutant la commande suivante :

```bash
pip install playwright beautifulsoup4 html5lib
```
Une fois les dépendances installées, tu dois également installer les navigateurs nécessaires pour Playwright. Exécute la commande suivante :

```bash
python -m playwright install
```
## Fonctionnement
Le script récupère les chemins de sauvegarde associés à un jeu vidéo depuis la page de son article sur** PCGamingWiki**. L'utilisateur entre l'URL du jeu, et le script extrait les informations de la page correspondant à cette URL.

## Étapes :
