import requests
from bs4 import BeautifulSoup


def scrape_vacatures(url: str, keywords: list[str], max_pages: int = 50) -> list[dict]:
    """
    Scraped vacatures van meerdere pagina's van een gegeven URL en filtert op keywords.

    Args:
        url (str): De basis-URL van de vacaturesite (zonder /pagina/).
        keywords (list[str]): Zoekwoorden om vacatures te filteren.
        max_pages (int): Het maximale aantal pagina's om te scrapen.

    Returns:
        list[dict]: Een lijst met dictionaries met vacature-informatie.
    """

    all_vacatures = []

    for page in range(1, max_pages + 1):
        try:
            # URL voor huidige pagina
            current_url = f'{url}/pagina/{page}'

            # Verstuur een GET-verzoek naar de URL
            response = requests.get(current_url)

            # Controleer of de pagina bestaat
            if response.status_code == 404:
                print(f"Pagina {page} bestaat niet. Stoppen met scrapen.")
                break

            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Fout bij het ophalen van data op psgins {page}: {e}")
            break

        # Parse de HTML van de pagina
        soup = BeautifulSoup(response.text, "html.parser")

        # Zoek vacatures in de HTML
        vacatures = []
        for item in soup.find_all("tr", class_="active"):
            try:
                # link vinden voor het ophalen van de gehele omschrijving
                link_tag = item.find("a", class_="row-link")
                link = f"https://www.banken.nl{link_tag['href']}" if link_tag and link_tag.get('href') else "Geen link beschikbaar"

                # Zoek de andere vereiste velden
                title = item.find("span", class_="title").text.strip()
                organization = item.find("span", class_="company").text.strip()
                vakgebied = item.find("a", class_="row-link initial").text.strip()
                vacature_type = item.find("td", class_="hide-tablet-landscape").text.strip()

                # Filter op zoekwoorden
                if any(keyword.lower() in title.lower() or keyword.lower() in organization.lower() for keyword in keywords):
                    vacatures.append({
                        "title": title,
                        "organization": organization,
                        "vakgebied": vakgebied,
                        "type": vacature_type,
                        "link": link
                    })
            except Exception as e:
                # Log de fout en ga verder met de volgende item
                print(f"Fout bij het verwerken van een vacature-item: {e}")
                continue

        # Voeg de vacatures van deze pagina toe aan de hoofdlijst
        if vacatures:
            all_vacatures.extend(vacatures)
        else:
            print(f"Geen vacatures gevonden op pagina {page}. Stoppen.")
            break

    return all_vacatures
