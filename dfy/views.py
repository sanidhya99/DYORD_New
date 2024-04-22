from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from .renderers import *
from .models import *
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import requests
from rest_framework import status
from .map_functions import *
import environ


env=environ.Env()

environ.Env.read_env()
api_key=env('Map_Api_Key')
class PlanCreate(generics.CreateAPIView):
    serializer_class = PlanSearializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [DFYRenderer]
    
    def post(self, request, *args, **kwargs):
        data=request.data
        origin = data.get('source')
        destinations = data.get('destination')
        prompt=f"tell me top 10 rated waypoints cities to have a hault in shortest route between {origin} to {destinations[0]} in a json format including waypoints,their rating and their consecutive travel time, their latitude, their longitude."
        URL = "https://api.openai.com/v1/chat/completions"
        payload = {
           "model": "gpt-3.5-turbo",
           "messages": [{"role": "user", "content": prompt}],
           "temperature" : 1.0,
           "top_p":1.0,
           "n" : 1,
           "stream": False,
           "presence_penalty":0,
           "frequency_penalty":0,
        }
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {env('ChatGPT_key')}"
        }
        try:
            response = requests.post(URL, headers=headers, json=payload, stream=False)
            print(response.json())
            waypoints_str = response.json()['choices'][0]['message']['content']
            start_index = waypoints_str.find('{')
            end_index = waypoints_str.rfind('}') + 1
            json_content = waypoints_str[start_index:end_index]
            waypointsinfo = json.loads(json_content)
            return Response(waypointsinfo,status=201)
        except:
            return Response({"error":"unable to fetch data"},status=404)
        
class PlanCreatePoints(generics.CreateAPIView):
    serializer_class = PlanSearializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [DFYRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Extract source and destination from the serializer's validated data
        source = serializer.validated_data.get('source')
        destinations = serializer.validated_data.get('destination')

        
        waypoints_info = {}

        # Get waypoints info for source and each consecutive pair of destinations
        for i in range(len(destinations) + 1):
            if i == 0:
                origin = source
            else:
                origin = destinations[i - 1]

            if i < len(destinations):
                destination = destinations[i]
            else:
                break  # Break if reached the end of destinations

            waypoints_key = f"Waypoints_{i}"
            waypoints_info[waypoints_key] = get_waypoints_info_points(api_key, origin, destination)

        # Return waypoints_info as a JSON response
        return Response(waypoints_info, status=status.HTTP_201_CREATED, headers=headers)    



class History(generics.ListAPIView):
    serializer_class = PlanSearializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [DFYRenderer]

    def get_queryset(self):
        user = self.request.user
        return Plan.objects.filter(user=user)


class restaurants(generics.ListAPIView):
    permission_classes=[IsAuthenticated,]
    renderer_classes=[DFYRenderer]
    def get(self, request, *args, **kwargs):

        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius')

        if not (latitude and longitude):
            return Response({'error': 'Latitude and longitude are required'}, status=400)

        url = "https://places.googleapis.com/v1/places:searchNearby"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "*"
        }

        data = {
            "includedTypes": ["restaurant"],
            "maxResultCount": 10,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": float(latitude),
                        "longitude": float(longitude)
                    },
                    "radius": float(radius)
                }
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            restaurants = []
            places_data = response.json().get('places', [])

            for place in places_data:
                if 'restaurant' in place['types']:
                    restaurant_info = {
                        'name': place['displayName']['text'],
                        'address': place['formattedAddress'],
                        'phone_number': place.get('internationalPhoneNumber'),
                        'rating': place.get('rating'),
                        'website': place.get('websiteUri'),
                        'location_url': f"https://www.google.com/maps?q={place['location']['latitude']},{place['location']['longitude']}"
                        # Add more fields as needed
                    }
                    restaurants.append(restaurant_info)

            return Response(restaurants)
        else:
            return Response({'error': 'Failed to fetch nearby restaurants'}, status=response.status_code)
class hotels(generics.ListAPIView):
    permission_classes=[IsAuthenticated,]
    renderer_classes=[DFYRenderer]
    def get(self, request, *args, **kwargs):

        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius')

        if not (latitude and longitude):
            return Response({'error': 'Latitude and longitude are required'}, status=400)

        url = "https://places.googleapis.com/v1/places:searchNearby"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "*"
        }

        data = {
            "includedTypes": ["lodging"],
            "maxResultCount": 10,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": float(latitude),
                        "longitude": float(longitude)
                    },
                    "radius": float(radius)
                }
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            hotels = []
            places_data = response.json().get('places', [])

            for place in places_data:
                if 'lodging' in place['types']:
                    hotel_info = {
                        'name': place['displayName']['text'],
                        'address': place['formattedAddress'],
                        'phone_number': place.get('internationalPhoneNumber'),
                        'rating': place.get('rating'),
                        'website': place.get('websiteUri'),
                        'location_url': f"https://www.google.com/maps?q={place['location']['latitude']},{place['location']['longitude']}"
                        # Add more fields as needed
                    }
                    hotels.append(hotel_info)

            return Response(hotels)
        else:
            return Response({'error': 'Failed to fetch nearby hotels'}, status=response.status_code)
            

class Events_endpoint(generics.ListAPIView):
    renderer_classes=[DFYRenderer]
    def get(self, request, *args, **kwargs):
        location = self.request.query_params.get('location')

        output=get_categories(location)

        return Response(output,status=200)
        
class News(generics.ListAPIView):
    renderer_classes=[DFYRenderer]
    def get(self, request, *args, **kwargs):
        location = request.query_params.get('location')
        url = "http://eventregistry.org/api/v1/article/getArticles"
        headers = {"Content-Type": "application/json"}
                
        # Request body
        payload = {
            "action": "getArticles",
            "keyword": f"{location} News",
            "articlesPage": 1,
            "articlesCount": 15,
            "articlesSortBy": "date",
            "articlesSortByAsc": False,
            "articlesArticleBodyLen": -1,
            "resultType": "articles",
            "dataType": ["news", "pr"],
            "apiKey": env('NEWS_KEY'),
            "forceMaxDataTimeWindow": 31
        }
        
        # Make the GET request
        response = requests.get(url, params=payload, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            articles = response.json()
            news = []
            for new in articles['articles']['results'] :
              news.append({'title' : new['title'], 'url' : new['url']})

            return Response({"data":news},status=200)
        else:
            return Response({"error":"No news found"},status=404)
            
        
