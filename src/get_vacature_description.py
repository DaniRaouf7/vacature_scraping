import requests
from bs4 import BeautifulSoup


def get_vacature_description(vacature_url: str) -> str:
    """
    Haalt de volledige vacatureomschrijving op van de vacaturepagina.

    Args:
        vacature_url (str): De URL van de vacaturepagina.

    Returns:
        str: De volledige tekst van de vacatureomschrijving of een foutmelding.
    """
    try:
        # Verstuur een GET-verzoek naar de URL
        response = requests.get(vacature_url)
        response.raise_for_status()

        # Parse de HTML van de pagina
        soup = BeautifulSoup(response.text, "html.parser")

        # Zoek de omschrijving
        description_tag = soup.find("div", class_="text imported")
        if description_tag:
            return description_tag.get_text(separator="\n", strip=True)
        else:
            return "Omschrijving niet gevonden"

    except Exception as e:
        print(f"Fout bij ophalen van {vacature_url}: {e}")
        return "Fout bij ophalen"
