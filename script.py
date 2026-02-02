import os
import requests
import tweepy
from datetime import date, timedelta

# URL de API Supabase
url = "https://pyicrgwkyiqbrlcoyqkh.supabase.co/rest/v1/prices"

# Récupérer les secrets pour l'API Supabase
API_KEY = os.environ.get('API_KEY')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

# Récupérer les secrets pour X
X_API_KEY = os.environ.get('X_API_KEY')
X_API_SECRET = os.environ.get('X_API_SECRET')
X_ACCESS_TOKEN = os.environ.get('X_ACCESS_TOKEN')
X_ACCESS_SECRET = os.environ.get('X_ACCESS_SECRET')

# Authentification X avec tweepy
client = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_SECRET
)
headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}',
    'apikey': API_KEY
}

aujourdhui = date.today().strftime('%Y-%m-%d')
demain = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

for jour in [aujourdhui, demain]:
    print(f"\n--- ANALYSE DU {jour} ---")

    response = requests.get(
        url,
        headers=headers,
        params={
            "select": "*",
            "day": "eq." + jour
        }
    )

    data = response.json()

    if data:
        resultat = data[0]
        
        for p in resultat['prices']:
            if p['best'] == True:
                meilleure_heure = f"{p['hour']} ({p['price_eur_per_kwh']} €/kWh)"
                print(f"L'heure la moins chère est : {meilleure_heure}")
                
        prix_min = resultat['summary']['min']
        prix_max = resultat['summary']['max']
        prix_moy = resultat['summary']['avg']

        print(f"Prix le plus bas : {prix_min} €/kWh")
        print(f"Prix le plus haut : {prix_max} €/kWh")
        print(f"Moyenne du jour : {prix_moy} €/kWh")
    else:
        print(f"Pas encore de données disponibles pour le {jour}.")
