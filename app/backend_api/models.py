from django.db import models

class Sample(models.Model):
    title = models.CharField(max_length = 100)
    channel = models.CharField(max_length=100)

class Courier(models.Model):
    courierID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    clientName = models.CharField(max_length=100)
    clientSurname = models.CharField(max_length=100)
    dependent = models.CharField(max_length=100)
    orderName = models.CharField(max_length=100) #название госулсгуи
    conBranch = models.CharField(max_length=100) 
    conAddress = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    courierID = models.ForeignKey(Courier, on_delete=models.CASCADE)
    