import requests
from datetime import date, timedelta
url = "https://pyicrgwkyiqbrlcoyqkh.supabase.co/rest/v1/prices"
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB5aWNyZ3dreWlxYnJsY295cWtoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODMwNTAwMCwiZXhwIjoyMDgzODgxMDAwfQ.JHyjMpxh-CJiRP5B_v7xzvCFaxIHGqEorK8P-ExYQrg",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB5aWNyZ3dreWlxYnJsY295cWtoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODMwNTAwMCwiZXhwIjoyMDgzODgxMDAwfQ.JHyjMpxh-CJiRP5B_v7xzvCFaxIHGqEorK8P-ExYQrg",
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
                print(f"L'heure la moins chère est : {p['hour']} ({p['price_eur_per_kwh']} €)")
                
        prix_min = resultat['summary']['min']
        prix_max = resultat['summary']['max']
        prix_moy = resultat['summary']['avg']

        print(f"Prix le plus bas : {prix_min} €/kWh")
        print(f"Prix le plus haut : {prix_max} €/kWh")
        print(f"Moyenne du jour : {prix_moy} €/kWh")
    else:
        print(f"Pas encore de données disponibles pour le {jour}.")