from django.shortcuts import render
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.views import APIView
from .models import Sample
from .serializer import SampleSerializer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

# from backend_api.models import Courier, Order
from backend_api.serializer import CourierSerializer, OrderSerializer

from backend_api.models import *
from backend_api.serializer import *
from django.core.files.storage import default_storage

# class SampleView(APIView):
#     def get(self, request):
#         # Handle GET request here
#         data = {"message": "Hello, World!"}
#         return Response(data, status=status.HTTP_200_OK)

#     def post(self, request):
#         # Handle POST request here
#         received_data = request.data # Assumes data is sent in JSON format
#         # Process received_data here
#         response_data = {"message": "Received and processed data successfully!"}
#         return Response(response_data, status=status.HTTP_201_CREATED)
    
@csrf_exempt
def courierApi(request):
    if request.method=='GET':
        courier = Courier.objects.all()
        courier_serializer = CourierSerializer(courier,many=True)
        res = JsonResponse(courier_serializer.data,safe=False)
        return res
    elif request.method == 'POST':
        courier_data=JSONParser().parse(request)
        courier_serializer=CourierSerializer(data=courier_data)
        if courier_serializer.is_valid():
            courier_serializer.save()
            return JsonResponse("Added successfully",safe=False)
        return JsonResponse("Failed to add", safe=False)

@csrf_exempt
def addCourierOrder(request):
    if request.method=='GET':
        order = Order.objects.all()
        order_serializer = OrderSerializer(order,many=True)
        return JsonResponse(order_serializer.data,safe=False)
    # elif request.method == 'POST':
    #     order_data=JSONParser().parse(request)
    #     order_serializer=OrderSerializer(data=order_data)
    #     if order_serializer.is_valid():
    #         order_serializer.save()
    #         return JsonResponse("Added successfully",safe=False)
    #     return JsonResponse("Failed to add", safe=False)
    elif request.method == 'POST':
        order_data=JSONParser().parse(request)
        order_serializer=OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order_serializer.save()
            return JsonResponse("Added successfully",safe=False)
        return JsonResponse("Failed to add", safe=False)
