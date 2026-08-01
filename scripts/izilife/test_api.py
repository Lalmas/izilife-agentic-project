import requests

KEY = "b38b73985dfb59e4ba5d7cabbe6cac18"  # remplace par ta vraie clé
headers = {"x-apisports-key": KEY}

r = requests.get("https://v3.football.api-sports.io/fixtures?league=61&season=2025", headers=headers)
print("Ligue 1 2025:", len(r.json().get("response", [])))

# CDM 2022 qui est terminée
r2 = requests.get("https://v3.football.api-sports.io/fixtures?league=1&season=2022", headers=headers)
print("CDM 2022:", len(r2.json().get("response", [])))