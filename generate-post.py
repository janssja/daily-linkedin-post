import os
import requests
import openai
from datetime import datetime, timedelta
from dotenv import load_dotenv
from llm_utils import create_chat_completion
from helpers import date_range, get_page_info, filter_func

# Load the environment variables from the .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_KEY")
model = "gpt-3.5-turbo"

# Replace with your own GOOGLE_API_KEY and CUSTOM_SEARCH_ENGINE_ID
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CUSTOM_SEARCH_ENGINE_ID = os.getenv("CUSTOM_SEARCH_ENGINE_ID")

# Define the date range
date_range = date_range()
now = datetime.now()

queries = [
    'News about ChatGPT GPT-4 in Health, Medicine, and Health Insurance',
    'Nieuws uit België en Nederland over ChatGPT en GPT-4 in Gezondheid, Geneeskunde en Ziektekostenverzekering',
    'Interesting use cases for ChatGPT and GPT-4',
]

results = []

for query in queries:
    params = {
        'key': GOOGLE_API_KEY,
        'cx': CUSTOM_SEARCH_ENGINE_ID,
        'q': query,
        'num': 7,
        'dateRestrict': 'd1',
        'sort': f'date:r:{date_range}'
    }

    try:
        response = requests.get('https://www.googleapis.com/customsearch/v1', params=params)
        results += response.json()['items']
    except:
        pass

filtered_results = filter(filter_func, results)

# Save hyperlinks to a file
with open(f"summaries/links-{now.strftime('%Y-%m-%d')}.txt", "w") as f:
    f.write(str(filtered_results))

# Summarize the content
summaries = []
timeout = 10

for i, result in enumerate(filtered_results):
    url = result['link']
    print(url)

    try:
        page = requests.get(url)
        gpt4_paragraphs = get_page_info(page)

        prompt = "\n".join([p.text for p in gpt4_paragraphs])

        with open(f"summaries/samenvatting-{i}.txt", "w") as f:
            f.write(prompt)

        messages = [
            {   
                "role": "system", 
                "content": "Je bent een professionele AI assistant gespecialiseerd in het schrijven van blogs. Je gebruikt een toon die wetenschappelijk en technisch is."
            },
            {
                "role": "user",
                "content": f"Maak een uitgebreide samenvatting in het Nederlands van de onderstaande tekst. Indien je geen samenvatting kunt maken, antwoord dan enkel met GEEN SAMENVATTING MOGELIJK.\n\nText: '''{prompt}'''"
            }
        ]


        summary = create_chat_completion(
            model=model,
            messages=messages,
            temperature=0.5,
            max_tokens=1500
        )

        if summary != "GEEN SAMENVATTING MOGELIJK":
            summaries.extend([url, summary])

    except requests.exceptions.Timeout:
        print(f"Timeout bereikt na {timeout} seconden.")
    except Exception as e:
        print(e)

with open(f"summaries/{now.strftime('%Y-%m-%d')}.txt", "w") as f:
    f.write(str(summaries))

# Create a single article
messages = [
    {   
        "role": "system", 
        "content": "Je bent een professionele AI assistant gespecialiseerd in het schrijven van blogs. Je gebruikt een toon die wetenschappelijk en technisch is."
    },
    {
        "role": "user",
        "content": f"Schrijf een professioneel Nederlandstalig LinkedIn-artikel over ChatGPT en GPT-4 op basis van de onderstaande samenvattingen. Het resultaat moet in Markdown-formaat zijn.\n\nSummaries: '''{summaries}'''"
    }
]


blogpost = create_chat_completion(
    model=model,
    messages=messages,
    temperature=0.5,
    max_tokens=2300
)

# Save the article to a file
print(blogpost)
with open(f"blogposts/{now.strftime('%Y-%m-%d')}.txt", "w") as f:
    f.write(blogpost)

params = {
    'key': GOOGLE_API_KEY,
    'cx': CUSTOM_SEARCH_ENGINE_ID,
    'q': 'The best GPT-4 prompt of this week',
    'num': 1,
    'dateRestrict': 'd1',
    'sort': f'date:r:{date_range}'
}

try:
    response = requests.get('https://www.googleapis.com/customsearch/v1', params=params)
    best_prompt = response.json()['items']
    with open(f"blogposts/prompt-of-the-week{now.strftime('%Y-%m-%d')}.txt", "w") as f:
        f.write(str(best_prompt))
except:
    pass

prompt = "Creeer een linkedin banner voor een blogpost over ChatGPT en GPT4"

response = openai.Image.create(
    prompt="Maak een linkedin banner voor een artikel over de laatste ontwikkelingen in chatGPT en GPT4",
    n=1,
    size="1024x1024"
)

image_url = response['data'][0]['url']

# Save the openAI banner from the response
with open(f"blogposts/{now.strftime('%Y-%m-%d')}.png", "wb") as f:
    f.write(requests.get(image_url).content)
