Daily LinkedIn Post Generator
Daily LinkedIn Post Generator is een Python-applicatie die gebruikmaakt van GPT-3.5-turbo van OpenAI en Google Custom Search om dagelijks relevante artikelen te vinden, samenvatten en een professioneel LinkedIn-artikel te genereren.

Installatie
Clone deze repository naar uw lokale machine:
bash
Copy code
git clone https://github.com/yourusername/daily-linkedin-post.git
Maak een virtuele omgeving en activeer deze:
bash
Copy code
python3 -m venv venv
source venv/bin/activate
Installeer de benodigde pakketten met behulp van pip:
bash
Copy code
pip install -r requirements.txt
Vraag API-sleutels aan voor zowel Google API als OpenAI API:

Google API Key: Volg de instructies in de Google API-documentatie
OpenAI API Key: Meld u aan of log in op OpenAI en zoek uw API-sleutel op de API-sleutelpagina.
Maak een .env-bestand in de hoofdmap van het project en voeg de volgende regels toe:

ini
Copy code
OPENAI_KEY=<uw-openai-api-sleutel>
GOOGLE_API_KEY=<uw-google-api-sleutel>
CUSTOM_SEARCH_ENGINE_ID=<uw-aangepaste-zoekmachine-id>
Vervang <uw-openai-api-sleutel>, <uw-google-api-sleutel> en <uw-aangepaste-zoekmachine-id> door uw daadwerkelijke API-sleutels en zoekmachine-ID.

Gebruik
Voer de applicatie uit met de volgende opdracht:

bash
Copy code
python generate-post.py
De applicatie zoekt naar relevante artikelen, genereert samenvattingen en creëert een LinkedIn-artikel in het Nederlands. De gegenereerde samenvattingen en het LinkedIn-artikel worden opgeslagen als tekstbestanden in de summaries en blogposts mappen.

De applicatie maakt ook een LinkedIn-banner en slaat deze op als een afbeeldingsbestand in de blogposts map.

Belangrijke opmerking
Het gebruik van de Google Custom Search API en OpenAI GPT-3.5-turbo kan kosten met zich meebrengen. Zorg ervoor dat u op de hoogte bent van de kosten voordat u deze applicatie uitvoert.
