from django.shortcuts import render
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.views import APIView
from .models import Sample
from .serializer import SampleSerializer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status


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
    
