from django.db import models

class Sample(models.Model):
    title = models.CharField(max_length = 100)
    channel = models.CharField(max_length=100)

class Courier(models.Model):
    courierID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    company = models.CharField(max_length=100, null=True)
    iin = models.CharField(max_length=100, null=True)

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    clientName = models.CharField(max_length=100)
    clientSurname = models.CharField(max_length=100)
    dependent = models.CharField(max_length=100, null=True)
    orderName = models.CharField(max_length=100) #название госулсгуи
    conBranch = models.CharField(max_length=100, null=True) 
    conAddress = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    iin = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=100)
    courierID = models.ForeignKey(Courier, on_delete=models.CASCADE)

class Con(models.Model):
    conID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100) 
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)

class Authentication(models.Model):
    authID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)