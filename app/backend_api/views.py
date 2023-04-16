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
import random

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

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
    
class Token(APIView):    

    def get_access_token(self, request):
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
            print(token)
            # Send GET request
            headers = {'Authorization': f'Bearer {token}'}
            response2 = requests.get('http://hakaton.gov4c.kz/api/bmg/check/010919600354', headers=headers)
            
            # Process response
            if response2.status_code == 200:
                # Do something with the response
                response_get = json.loads(response2.content)
                phone = response_get.get('phone')
                print(phone)
                print(f'{phone}')
                my_id = response_get.get('id')
                
                code = str(random.randint(1000, 9999))
                
                #IF STATEMENT TO CHECK UNIQUNESS OF THE CODE IN THE DATABASE
                
                if Order.objects.filter(code=code).exists():
                    # return an error message if the user already exists
                    code = str(random.randint(1000, 9999))
                    # my_object = Order.objects.get(courierID_id=my_id)
                    # my_value = "New value"
                    # query = "UPDATE backend_api_order SET code=%s WHERE id=%s;"
                    # with connection.cursor() as cursor:
                    # cursor.execute(query, [my_value, my_id])
                    try:
                        my_object = Order.objects.get(courierID=5)
                    except Order.DoesNotExist:
                        # Handle the case when the object does not exist
                        return JsonResponse({'error': 'Object not found.'}, status=404)
                    print(my_object)
                    my_object.code = code
                    my_object.save()

                try:
                    order = Order.objects.get(courierID=5)
                except Order.DoesNotExist:
                    # Handle the case when the object does not exist
                    return JsonResponse({'error': 'Object not found.'}, status=404)
                order_serializer = CourierOrderSerializer(order,many=True)
                if order_serializer.is_valid():
                    order.code = code 

                    # Save the object to the database
                    order.save()
                    # return JsonResponse({'status': 'error', 'message': 'Username already exists.'},safe=False)
                # create a new user object and save it to the database
                # user = Authentication(code=code, password=password)
                # user.save()

                # # return a success message
                # return JsonResponse({'status': 'success', 'message': 'User created successfully.'},safe=False)

                url = 'http://hak-sms123.gov4c.kz/api/smsgateway/send'
                headers = {
                    'Content-Type': 'application/json' ,
                    'Authorization': f'Bearer {token}'
                }
                data = {
                    "phone" : f"{phone}",
                    "smsText" : "Код для выдачи документов - "+f"{code}"+". Сообщите его только сотруднику ЦОНа и никому больше!"
                }
                response_sms = requests.post('http://hak-sms123.gov4c.kz/api/smsgateway/send', data=json.dumps(data), headers=headers)
                print(response_sms.status_code)
                if response_sms.status_code == 200:
                    return JsonResponse(response_sms.json())
                else:
                    return JsonResponse({'error': response_sms.status_code}, status=response_sms.status_code)
            else:
                 # Handle error
                 return JsonResponse({'error': 'Something went wrong2'}, status=response2.status_code)
        else:
                return JsonResponse({'error': 'Something went wrong'}, status=response.status_code)

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
def conApi(request):
    if request.method=='GET':
        con = Con.objects.all()
        con_serializer = ConSerializer(con,many=True)
        res = JsonResponse(con_serializer.data,safe=False)
        return res
    elif request.method == 'POST':
        con_data=JSONParser().parse(request)
        con_serializer=ConSerializer(data=con_data)
        if con_serializer.is_valid():
            con_serializer.save()
            return JsonResponse("Added successfully",safe=False)
        return JsonResponse("Failed to add", safe=False)

@csrf_exempt
def addCourierOrder(request):
    if request.method=='GET':
        order = Order.objects.all()
        order_serializer = CourierOrderSerializer(order,many=True)
        return JsonResponse(order_serializer.data,safe=False)
    elif request.method == 'POST':
        order_data=JSONParser().parse(request)
        order_serializer=CourierOrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order_serializer.save()
            return JsonResponse("Added successfully",safe=False)
        return JsonResponse("Failed to add", safe=False)

@csrf_exempt  
def authentication(request):
    if request.method=='GET':
        auth = Authentication.objects.all()
        auth_serializer = AuthenticationSerializer(auth,many=True)
        res = JsonResponse(auth_serializer.data,safe=False)
        return res
    elif request.method == 'POST':
        auth_data=JSONParser().parse(request)
        auth_serializer=AuthenticationSerializer(data=auth_data)
        if auth_serializer.is_valid():
            auth_serializer.save()
            return JsonResponse("Added successfully",safe=False)
        return JsonResponse("Failed to add", safe=False)
    

    # {'id': 5, 'iin': '930823300880', 'code': '12', 'phone': '87769864618'}
@csrf_exempt
def courierSms(request):
    if request.method == 'POST':
        postdata = JSONParser().parse(request)
        var = Token()
        variable = var.get_access_token(request)

        # Check if Order with the given courierID_id exists
        try:
            order = Order.objects.get(courierID_id=postdata['courierID'])
        except Order.DoesNotExist:
            # Handle the case when the object does not exist
            return JsonResponse({'error': 'Object not found.'}, status=404)

        # Update the 'code' field in the Order model with the new code
        new_code = postdata.get('code')
        if new_code:
            order.code = new_code
            order.save()

            # Send SMS
            return JsonResponse({'status': 'success', 'message': 'SMS sent successfully.'})
        else:
            # Handle the case when the new code is not provided
            return JsonResponse({'error': 'New code is not provided.'}, status=400)
    
    # Return an error message for other HTTP methods
    return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)


        
    
@csrf_exempt
def create_user(request):
    # if request.method == 'POST':
    #     # get the username and password from the request POST data
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     print(username, password)

    #     # check if the user already exists
    #     if Authentication.objects.filter(username=username).exists():
    #         # return an error message if the user already exists
    #         return JsonResponse({'status': 'error', 'message': 'Username already exists.'},safe=False)

    #     # create a new user object and save it to the database
    #     user = Authentication(username=username, password=password)
    #     user.save()

    #     # return a success message
    #     return JsonResponse({'status': 'success', 'message': 'User created successfully.'},safe=False)
    # return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    if request.method == 'POST':
        user_data=JSONParser().parse(request)
        print(user_data)
        username = user_data['username']
        password = user_data['password']
        print(username)
        if Authentication.objects.filter(username=username).exists():
            # return an error message if the user already exists
            return JsonResponse({'status': 'error', 'message': 'Username already exists.'},safe=False)
        
        # create a new user object and save it to the database
        user = Authentication(username=username, password=password)
        user.save()

        # return a success message
        return JsonResponse({'status': 'success', 'message': 'User created successfully.'},safe=False)
    if request.method=='GET':
        auth = Authentication.objects.all()
        auth_serializer = AuthenticationSerializer(auth,many=True)
        res = JsonResponse(auth_serializer.data,safe=False)
        return res
    

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
    
