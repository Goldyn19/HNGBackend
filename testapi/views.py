import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import TestSerializer

class HelloAPIView(APIView):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_location(self, ip):
        ipinfo_url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(ipinfo_url)
        data = response.json()
        return data

    def get_weather(self, city):
        api_key = '30d26fa8203097de174999f65a65a640'
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
        response = requests.get(weather_url)
        data = response.json()
        return data

    def get(self, request):
        serializer = TestSerializer(data=request.GET)
        if serializer.is_valid():
            visitor_name = serializer.validated_data.get('visitor_name', 'Guest')
            client_ip = self.get_client_ip(request)
            location_data = self.get_location(client_ip)
            city = location_data.get('city', 'Unknown')
            weather_data = self.get_weather(city)
            temperature = weather_data['main']['temp'] if 'main' in weather_data else 'N/A'

            response_data = {
                'client_ip': client_ip,
                'location': city,
                'greeting': f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {city}."
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
