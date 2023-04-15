from django.shortcuts import render
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.views import APIView
from .models import Sample
from .serializer import SampleSerializer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status
import requests

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class SampleView(APIView):
    def get(self, request):
        # Handle GET request here
        data = {"message": "Hello, World!"}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # Handle POST request here
        received_data = request.data # Assumes data is sent in JSON format
        # Process received_data here
        response_data = {"message": "Received and processed data successfully!"}
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class Token(APIView):

    """ def get_token(request):
        received_data = request.data # Assumes data is sent in JSON format
        # Process received_data here
        response_data = {"message": "Received and processed data successfully!"}
        url = "http://hakaton-idp.gov4c.kz/auth/realms/con-web/protocol/openid-connect/token"
        data = {
            "username": "test-operator",
            "password": "DjrsmA9RMXRl",
            "client_id": "cw-queue-service",
            "grant_type": "password"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url, data=data, headers=headers)
        return Response(response.json().get("access_token")) """
    
    

    def get_access_token(request):
        url = 'http://hakaton-idp.gov4c.kz/auth/realms/con-web/protocol/openid-connect/token'
        data = {
            'username': 'test-operator',
            'password': 'DjrsmA9RMXRl',
            'client_id': 'cw-queue-service',
            'grant_type': 'password'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            response_json = json.loads(response.content)
            token = response_json.get('access_token')
            
            # Send GET request
            headers = {'Authorization': f'Bearer {token}'}
            response2 = requests.get('http://hakaton.gov4c.kz/api/bmg/check/010919600354', headers=headers)
            
            # Process response
            if response2.status_code == 200:
                # Do something with the response
                response_get = json.loads(response2.content)
                phone = response_get.get('phone')
                print(phone)
                url = 'http://hakaton-sms.gov4c.kz/api/smsgateway/send'
                data = {
                    "phone" : f'{phone}',
                    "smsText" : "Hello World!"

                }
                headers = {
                    'Content-Type': 'application/json' ,
                    'Authorization': f'Bearer {token}'
                }

                response_sms = requests.post(url, data=data, headers=headers)
                if response_sms.status_code == 200:
                    return JsonResponse(response_sms.json())
                else:
                    return JsonResponse(response2.json())
            else:
                # Handle error
                return JsonResponse({'error': 'Something went wrong2'}, status=response2.status_code)
        else:
            return JsonResponse({'error': 'Something went wrong'}, status=response.status_code)



    