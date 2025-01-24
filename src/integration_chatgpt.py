import os
import openai
import json
import pandas as pd
from dotenv import load_dotenv


# Laden API-key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_job_details(description):
    prompt = f"""
    Analyseer de volgende vacaturetekst en haal de onderstaande informatie op:
    Zorg ervoor dat je alleen de gevraagde informatie ophaalt en geen extra kolommen toevoegt.
    Geef het antwoord in JSON-formaat met precies de volgende 10 kolommen, zoals in het voorbeeld hieronder:
    Wanneer een bepaald veld niet gevonden kan worden, geef dan een lege string of "Niet gevonden" terug.

    1. Vereiste vaardigheden (hard skills)
    2. Vereiste vaardigheden (soft skills)
    3. Aantal jaren ervaring
    4. Opleidingsniveau
    5. Salarisindicatie (Alleen wanneer vermeld)
    6. Locatie
    7. Type dienstverband (bijv. fulltime, parttime, freelance)
    8. Belangrijke contactpersoon naam en achternaam (Indien gevonden)
    9. Belangrijk contactpersoon zijn email (Indien gevonden)
    10. Belangrijk contactpersoon zijn 06 (Indien gevonden)

    Dit is een voorbeeld van het JSON-formaat waarop je moet letten:

    {{
        "Vereiste vaardigheden (hard skills)": "Python, SQL, Data Analysis",
        "Vereiste vaardigheden (soft skills)": "Communication, Teamwork",
        "Aantal jaren ervaring": "5",
        "Opleidingsniveau": "Bachelor",
        "Salarisindicatie": "€3500",
        "Locatie": "Amsterdam",
        "Type dienstverband": "Fulltime",
        "Belangrijke contactpersoon naam en achternaam": "Jan Jansen",
        "Belangrijk contactpersoon zijn email": "jan.jansen@email.com",
        "Belangrijk contactpersoon zijn 06": "0612345678"
    }}

    Vacaturetekst:
    {description}

    Geef alleen deze 10 velden terug in **exact hetzelfde formaat** als het voorbeeld, zonder extra velden of informatie.
    Wanneer een bepaald veld niet gevonden kan worden, geef dan een lege string of "Niet gevonden" terug.
    """

    try:
        client = openai.OpenAI()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Je bent een AI die vacatureteksten analyseert en gestructureerde informatie teruggeeft."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        # OpenAI geeft een string terug, dus we converteren het naar een Python dictionary
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"Fout bij OpenAI-analyse: {e}")
        return None


def process_vacatures(df):
    """
    Verwerkt de vacatures één voor één en haalt de gestructureerde gegevens op via ChatGPT.
    """
    analyse_resultaten = []
    for description in df['Volledige Functie omschrijving']:
        if description == "Omschrijving niet gevonden":  # Controleer of de omschrijving ontbreekt
            print("Vacature zonder omschrijving, sla deze over.")
            analyse_resultaten.append({"error": "Omschrijving niet gevonden"})  # Voeg de foutmelding toe
        else:
            result = extract_job_details(description)
            analyse_resultaten.append(result)
    # Zet de resultaten om in een DataFrame van gestructureerde gegevens
    return pd.json_normalize(analyse_resultaten)
