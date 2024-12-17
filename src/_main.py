import pandas as pd
from src.scraping import scrape_vacatures
from src.get_vacature_description import get_vacature_description


def main():
    """
    Startpunt van de applicatie. Roept de scrape-functie aan.
    """
    # Website en filtercriteria instellen
    url = "https://banken.nl/vacatures"
    keywords = ["data", "engineer", "analyst", "analist", "machine", "business", "developer"]
    target_organizations = ['abn amro', 'rabobank', 'dpa', 'de nederlandsche bank', 'bng bank', 'volksbank']
    file_path_excel = r"C:\Users\danis\vacatures_zoeken\voorbeeld_excel\vacatures_banken_nl_eindbestand.xlsx"

    # Data scrapen
    try:
        scraped_data = scrape_vacatures(url, keywords)
        if not scraped_data:
            print("Geen vacatures gevonden.")
            return

        # nodige transformaties
        df_vacatures_banken_nl = pd.DataFrame(scraped_data)
        df_vacatures_banken_nl = df_vacatures_banken_nl[df_vacatures_banken_nl['organization'].str.lower().isin([org.lower() for org in target_organizations])]
        df_vacatures_banken_nl = df_vacatures_banken_nl.fillna(value='Onbekend')
        df_vacatures_banken_nl['Volledige Functie omschrijving'] = df_vacatures_banken_nl['link'].apply(get_vacature_description)


        # Wegschrijven naar een excel bestand
        df_vacatures_banken_nl.to_excel(file_path_excel, index=False)
        print(f"Data opgeslagen in {file_path_excel}")

    except Exception as e:
        print(f"Fout bij het uitvoeren van het programma: {e}")


if __name__ == "__main__":
    main()
