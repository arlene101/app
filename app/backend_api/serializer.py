from rest_framework import serializers
from .models import Sample, Courier, Order

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