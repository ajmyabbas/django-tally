from django.db import models

# Create your models here.
class CreateStockGrp(models.Model):
    name=models.CharField(max_length=100)
    alias=models.CharField(max_length=100)
    under_name=models.CharField(max_length=50)
    quantities=models.CharField(max_length=50)
    
class CreateStockCateg(models.Model):
    name=models.CharField(max_length=100)
    alias=models.CharField(max_length=100)
    under_name=models.CharField(max_length=50)
    quantities=models.CharField(max_length=50)

class stock_item_crt(models.Model):
    name=models.CharField(max_length=100,null=True)
    alias=models.CharField(max_length=100,null=True)
    under=models.CharField(max_length=100,null=True)
    category=models.CharField(max_length=100,null=True)
    units=models.CharField(max_length=100,null=True)
    batches=models.CharField(max_length=100,null=True)
    manufacturing_date=models.CharField(max_length=100,null=True)
    expiry_dates=models.CharField(max_length=100,null=True)
    rate_of_duty=models.CharField(max_length=100,null=True)
    quantity=models.CharField(max_length=100,null=True)
    rate=models.CharField(max_length=100,null=True)
    per=models.CharField(max_length=100,null=True)
    value=models.CharField(max_length=100,null=True)    