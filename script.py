import os
import requests
import tweepy
from datetime import date, timedelta, datetime
import sys

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

def poster_tweet(texte):
    """Poste un tweet via tweepy"""
    try:
        response = client.create_tweet(text=texte)
        print(f"✅ Tweet posté avec succès (ID: {response.data['id']})")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la publication : {e}")
        return False

def get_prix_jour(jour_str):
    """Récupère les prix pour un jour donné"""
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
        'apikey': API_KEY
    }
    
    response = requests.get(
        url,
        headers=headers,
        params={
            "select": "*",
            "day": "eq." + jour_str
        }
    )
    data = response.json()
    
    if data:
        return data[0]
    return None

def formater_date_espagnol(date_str):
    """Convertit 2025-02-03 en format espagnol : lunes 3 de febrero"""
    # Jours et mois en espagnol
    jours = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    mois = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
            'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    jour_semaine = jours[dt.weekday()]
    mois_nom = mois[dt.month - 1]
    
    return f"{jour_semaine} {dt.day} de {mois_nom}"

def tweet_deja_poste_aujourdhui():
    """Vérifie si un tweet a déjà été posté pour aujourd'hui"""
    try:
        # Récupérer l'ID de l'utilisateur
        me = client.get_me()
        user_id = me.data.id
        
        # Récupérer les 10 derniers tweets
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=10,
            tweet_fields=['created_at', 'text']
        )
        
        aujourdhui = date.today().strftime('%Y-%m-%d')
        date_formatee = formater_date_espagnol(aujourdhui)
        
        if tweets.data:
            for tweet in tweets.data:
                # Vérifier si la date du jour est dans le texte du tweet
                if date_formatee in tweet.text:
                    print(f"✅ Tweet déjà posté pour {date_formatee}")
                    return True
        
        print(f"ℹ️ Aucun tweet trouvé pour {date_formatee}")
        return False
        
    except Exception as e:
        print(f"⚠️ Erreur lors de la vérification : {e}")
        # En cas d'erreur, on poste quand même pour ne pas rater le tweet
        return False

# Récupérer l'argument de type de tweet
type_tweet = sys.argv[1] if len(sys.argv) > 1 else "demain"

if type_tweet == "demain":
    # Tweet du soir pour le lendemain (21h)
    demain = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"\n--- TWEET POUR DEMAIN ({demain}) ---")
    
    resultat = get_prix_jour(demain)
    
    if resultat:
        # Récupérer la meilleure heure
        meilleure_heure = None
        meilleur_prix = None
        for p in resultat['prices']:
            if p['best'] == True:
                meilleure_heure = p['hour']
                meilleur_prix = p['price_eur_per_kwh']
        
        prix_moy = resultat['summary']['avg']
        date_formatee = formater_date_espagnol(demain)
        
        tweet = f"""⚡ Precio de la luz – {date_formatee}

💰 Precio medio: {prix_moy} €/kWh
🕐 Hora más barata: {meilleure_heure} ({meilleur_prix} €/kWh)

Consulta todos los precios oficiales #PVPC hora a hora con #LuzHoyApp, un servicio de @papernest_es

📲 Descarga la app https://papernest.app/luzhoy"""
        
        print(tweet)
        poster_tweet(tweet)
    else:
        print(f"Pas encore de données pour demain ({demain})")

elif type_tweet == "aujourdhui":
    # Tweet du matin pour aujourd'hui (7h)
    aujourdhui = date.today().strftime('%Y-%m-%d')
    print(f"\n--- TWEET POUR AUJOURD'HUI ({aujourdhui}) ---")
    
    # Vérifier si le tweet a déjà été posté hier soir
    if tweet_deja_poste_aujourdhui():
        print("🚫 Tweet déjà posté hier soir, abandon du tweet du matin")
        sys.exit(0)
    
    resultat = get_prix_jour(aujourdhui)
    
    if resultat:
        # Récupérer la meilleure heure
        meilleure_heure = None
        meilleur_prix = None
        for p in resultat['prices']:
            if p['best'] == True:
                meilleure_heure = p['hour']
                meilleur_prix = p['price_eur_per_kwh']
        
        prix_moy = resultat['summary']['avg']
        date_formatee = formater_date_espagnol(aujourdhui)
        
        tweet = f"""⚡ Precio de la luz – {date_formatee}

💰 Precio medio: {prix_moy} €/kWh
🕐 Hora más barata: {meilleure_heure} ({meilleur_prix} €/kWh)

Consulta todos los precios oficiales #PVPC hora a hora con #LuzHoyApp, un servicio de @papernest_es

📲 Descarga la app https://papernest.app/luzhoy"""
        
        print(tweet)
        poster_tweet(tweet)
    else:
        print(f"Pas de données pour aujourd'hui ({aujourdhui})")
