import requests
from bs4 import BeautifulSoup
def get_directions(api_key, origin, destination):
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "key": api_key,
        "origin": origin,
        "destination": destination,
        "mode": "driving"
    }

    response = requests.get(base_url, params=params)
    print(response.json())
    return response.json()

def get_waypoints_info(api_key, origin, destination):

    directions = get_directions(api_key, origin, destination)
    waypoints_info = []

    if 'routes' in directions and len(directions['routes']) > 0:
        legs = directions['routes'][0]['legs']
        waypoints = [step['end_location'] for leg in legs for step in leg['steps'][:-1]]
        # print(f"waypoints initial: {waypoints}")
        for i, waypoint in enumerate(waypoints):
            waypoint_lat = waypoint['lat']
            waypoint_lng = waypoint['lng']

            base_url_directions = "https://maps.googleapis.com/maps/api/directions/json"
            params_directions = {
                "key": api_key,
                "origin": origin,
                "destination": f"{waypoint_lat},{waypoint_lng}",
                "mode": "driving"
            }

            response_directions = requests.get(base_url_directions, params=params_directions)
            if 'routes' in response_directions.json() and len(response_directions.json()['routes']) > 0:
                legs_directions = response_directions.json()['routes'][0]['legs']
                travel_time = legs_directions[0]['duration']['text']

                base_url_places = "https://maps.googleapis.com/maps/api/geocode/json"
                params_places = {
                    "key": api_key,
                    "latlng": f"{waypoint_lat},{waypoint_lng}",
                }

                response_places = requests.get(base_url_places, params=params_places)
                if 'results' in response_places.json() and len(response_places.json()['results']) > 0:
                    name = response_places.json()['results'][0].get('formatted_address', 'Unnamed')
                else:
                    name = f"Waypoint {i + 1}"

                waypoint_info = {
                    'name': name,
                    'lat': waypoint_lat,
                    'lng': waypoint_lng,
                    'travel_time': travel_time
                }

                base_url_rating = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
                params_rating = {
                    "key": api_key,
                    "input": f"{name}",
                    "inputtype": "textquery",
                    "fields": "rating"
                }

                response_rating = requests.get(base_url_rating, params=params_rating)
                if 'candidates' in response_rating.json() and len(response_rating.json()['candidates']) > 0:
                    rating = response_rating.json()['candidates'][0].get('rating', 'No rating')
                else:
                    rating = 'No rating'

                waypoint_info['rating'] = rating
                waypoints_info.append(waypoint_info)
                # print(waypoint_info)
    # print(waypoint_info)
    waypoints_info_filtered = [
        waypoint for waypoint in waypoints_info 
        if 'rating' in waypoint and (
            float(waypoint['rating']) > 4 if waypoint['rating'] != 'No rating' else False
        )
    ]            
    return waypoints_info_filtered


def get_waypoints_info_points(api_key, origin, destination):
    directions = get_directions(api_key, origin, destination)

    if 'routes' in directions and len(directions['routes']) > 0:
        legs = directions['routes'][0]['legs']
        waypoints = [step['end_location'] for leg in legs for step in leg['steps'][:-1]]

    return waypoints    

def get_categories(location):
    url = 'https://insider.in/'+location
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = []
    cards =  (soup.find('ul', {'class': 'card-list css-0'})).find_all('a')
    for i in cards:
      if 'https' not in i['href']:
        url = 'https://insider.in'+i['href']
        response_1 = requests.get(url)
        soup1 = BeautifulSoup(response_1.text)
        more_events = soup1.find_all('li',{'class':'card-list-item'})
        if len(more_events) != 0 and more_events[0].find('a') is not None:
          for j in more_events:
            if j.find('a') is not None:
              if location in (j.find('a'))['href']:
                categories.append('https://insider.in'+ (j.find('a'))['href'])
        else:
          categories.append(url)
    output = {}

    for cat in range(len(categories)):

      response = requests.get(categories[cat])

      soup = BeautifulSoup(response.text,'html.parser')

      script_tag = soup.find('script', {'data-react-helmet': 'true', 'type': 'application/ld+json'})

      if script_tag:
          script_content = script_tag.string
          output[categories[cat]] = script_content

    return output