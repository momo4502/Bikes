
import requests

# Clé API pour accéder à l'API JCDecaux
api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"

# Fonction pour récupérer les données des stations de vélos via l'API JCDecaux
def get_bike_data():
    bike_data = []
    url = "https://api.jcdecaux.com/vls/v3/stations?apiKey=e0a1bf2c844edb9084efc764c089dd748676cc14"
    response = requests.get(url)
    for station in response.json():
        city = station.get('city', '')
        mechanical_bikes = station['mainStands']['availabilities'].get('mechanical', 0)
        electric_bikes = station['mainStands']['availabilities'].get('electric', 0)
        bike_data.append({'name': station['name'], 'city': city, 'mechanical_bikes': mechanical_bikes, 'electric_bikes': electric_bikes})
    return bike_data

# Appeler la fonction pour récupérer les données des stations de vélos
bike_data = get_bike_data()

# Fonction pour calculer le pourcentage de vélos mécaniques et électriques en fonction des villes
def calculate_bike_percentage(bike_data):
    city_bikes = {}
    
    for station in bike_data:
        city = station['city']
        if city not in city_bikes:
            city_bikes[city] = {'mechanical': 0, 'electric': 0}
        city_bikes[city]['mechanical'] += station['mechanical_bikes']
        city_bikes[city]['electric'] += station['electric_bikes']
    for city in city_bikes:
        total_bikes = city_bikes[city]['mechanical'] + city_bikes[city]['electric']
        if total_bikes > 0:
            mechanical_percentage = (city_bikes[city]['mechanical'] / total_bikes) * 100
            electric_percentage = (city_bikes[city]['electric'] / total_bikes) * 100
            city_bikes[city]['mechanical_percentage'] = mechanical_percentage
            city_bikes[city]['electric_percentage'] = electric_percentage
        else:
            city_bikes[city]['mechanical_percentage'] = 0
            city_bikes[city]['electric_percentage'] = 0
    return city_bikes


# Fonction pour classer les villes avec le plus de vélos
def get_city_ranking(city_bikes):
    city_ranking = sorted(city_bikes.items(), key=lambda x: x[1]['mechanical'] + x[1]['electric'], reverse=True)
    return city_ranking

# Récupération des données des stations de vélos via l'API JCDecaux
bike_data = get_bike_data()

# Calcul du pourcentage de vélos mécaniques et électriques en fonction des villes
city_bikes = calculate_bike_percentage(bike_data)

# Classement des villes avec le plus de vélos
city_ranking = get_city_ranking(city_bikes)

# Affichage des résultats
print("Pourcentage de vélos mécaniques et électriques en fonction des villes:")
for city in city_bikes:
    print(city, " - mécanique:", round(city_bikes[city]['mechanical_percentage'], 2), "%", " - électrique:", round(city_bikes[city]['electric_percentage'], 2), "%")
    
print("\nClassement des villes avec le plus de vélos:")
for i in range(len(city_ranking)):
    print(i+1, ".", city_ranking[i][0], " - total:", round(city_ranking[i][1]['mechanical_percentage'] + city_ranking[i][1]['electric_percentage'], 2), "%")

