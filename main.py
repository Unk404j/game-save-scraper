import asyncio  # Importation de la bibliothèque asyncio pour gérer les appels asynchrones
from bs4 import BeautifulSoup  # Importation de BeautifulSoup pour analyser le contenu HTML
from playwright.async_api import async_playwright  # Importation de la bibliothèque Playwright pour contrôler un navigateur de manière asynchrone
import re  # Importation de la bibliothèque re pour manipuler les chaînes de caractères

# Informations d'authentification pour se connecter à un proxy de scraping
# AUTH = 'brd-customer-hl_f873ba8f-zone-scraping_browser1:kmv62akub0q9'
# Exemple avec un proxy anonyme
SBR_WS_CDP = 'localhost'

# Demande à l'utilisateur d'entrer l'URL d'une page de jeu sur PCGamingWiki
url = input("Entrez l'url du jeu :\n")

# Fonction pour extraire les chemins de sauvegarde depuis le HTML d'une page
def extract_savepath(html):
    bs = BeautifulSoup(html, 'html5lib')
    headline = bs.find("span", class_="mw-headline", id="Save_game_data_location")

    if headline:
        container = headline.find_parent("h3").find_next("div", class_="container-pcgwikitable")
        if container:
            rows = container.find_all("tr", class_="template-infotable-body table-gamedata-body-row")
            savepaths = []
            for row in rows:
                location_cell = row.find("td", class_="table-gamedata-body-location")
                if location_cell:
                    savepath = location_cell.get_text(strip=True)
                    savepaths.append(savepath)
            return savepaths
    return []

# Nettoyer l'URL pour créer un nom de fichier valide
def sanitize_filename(url):
    return re.sub(r'[<>:"/\\|?*]', '_', url) + ".txt"

# Fonction principale pour exécuter le processus de scraping
async def run(pw):
    print('Launching browser...')
    browser = await pw.chromium.launch(headless=False)  # Lance le navigateur en mode non headless
    try:
        page = await browser.new_page()
        print('Navigating to webpage')

        await page.goto(url)

        html = await page.content()

        savepaths = extract_savepath(html)

        print(savepaths)

        filename = sanitize_filename(url)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(savepaths))
    finally:
        await browser.close()


# Fonction principale d'exécution asynchrone
async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())
