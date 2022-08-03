from django.db import models

# Create your models here.
class StockGroup(models.Model):
    grp_name = models.CharField(max_length=70, null=False, blank=False)

    def __str__(self):
        return self.grp_name

class CreateStockGrp(models.Model):
    name=models.CharField(max_length=100)
    alias=models.CharField(max_length=100)
    quantities=models.CharField(max_length=50)
    group = models.ForeignKey(StockGroup,on_delete=models.SET_NULL, null=True)
    
class CreateStockCateg(models.Model):
    name=models.CharField(max_length=100)
    alias=models.CharField(max_length=100)
    under_name=models.CharField(max_length=50)
    quantities=models.CharField(max_length=50)

class stock_item(models.Model):
    name=models.CharField(max_length=100,null=True)
    alias=models.CharField(max_length=100,null=True)
    quantity=models.CharField(max_length=100,null=True)
    rateper=models.CharField(max_length=100,null=True)
    value=models.CharField(max_length=100,null=True)    
    group = models.ForeignKey(StockGroup,on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        return self.name

class voucherlist(models.Model):
    item = models.ForeignKey(stock_item,on_delete=models.SET_NULL, null=True) 
    party_name=models.CharField(max_length=100,null=True)
    vouch_type=models.CharField(max_length=100,null=True)
    date=models.DateField()
    quantity=models.IntegerField()
    rateper=models.CharField(max_length=100,null=True)
    value=models.IntegerField() 