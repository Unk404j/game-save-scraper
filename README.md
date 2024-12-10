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
1. L'utilisateur entre l'URL d'un jeu PCGamingWiki dans le terminal.
2. Le script lance un navigateur Chromium en mode non headless (avec interface graphique) pour charger la page.
3. Le script recherche les données de sauvegarde du jeu dans le HTML de la page à l'aide de BeautifulSoup.
4. Il extrait et affiche les chemins de sauvegarde trouvés, puis les écrit dans un fichier texte dont le nom est basé sur l'URL du jeu.

# Fonctionnalités
## Fonction principale
- ```run(pw)``` : Gère le processus de scraping, en lançant un navigateur et en naviguant vers l'URL fournie. Il récupère ensuite le contenu HTML de la page, extrait les informations de sauvegarde et les écrit dans un fichier.
## Nettoyage des noms de fichier
```sanitize_filename(url)``` : Cette fonction nettoie l'URL fournie pour la convertir en un nom de fichier valide. Elle remplace les caractères non autorisés par des underscores (```_```).

# Exécution du script
Pour exécuter le script, il suffit de l'exécuter dans un terminal :
```python scraper.py```

## Exemple :
Si tu exécutes le script et entres l'URL suivante :
```https://www.pcgamingwiki.com/wiki/Game_Name```
