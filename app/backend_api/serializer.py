from rest_framework import serializers
from .models import *

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ['title','channel']

class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ['courierID','name','surname','phone']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['orderID','clientName','clientSurname','dependent','orderName','conBranch','conAddress','time']

class ConSerializer(serializers.ModelSerializer):
    class Meta:
        model = Con
        fields = ['conID','name','surname','phone','email']

class AuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authentication
        fields = ['username','password']

class CourierOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['orderID','clientName','clientSurname','dependent','orderName','conBranch','conAddress','time','iin','code','courierID']