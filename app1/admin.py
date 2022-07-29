from django.contrib import admin
from app1.models import CreateStockGrp,CreateStockCateg,stock_item
# Register your models here.
@admin.register(CreateStockGrp)
class stockgrpadmin(admin.ModelAdmin):
    list_display = ('id','name','alias','under_name','quantities')

@admin.register(CreateStockCateg)
class CreateStockCategadmin(admin.ModelAdmin):
    list_display = ('id','name','alias','under_name','quantities')    

@admin.register(stock_item)
class stock_itemadmin(admin.ModelAdmin):
    list_display = ('id','name','alias','under','quantity','rateper','value')      

