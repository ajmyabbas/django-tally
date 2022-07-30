from django.contrib import admin
from app1.models import CreateStockGrp,CreateStockCateg, StockGroup,stock_item
# Register your models here.
@admin.register(CreateStockGrp)
class stockgrpadmin(admin.ModelAdmin):
    list_display = ('id','name','alias','quantities','group')

@admin.register(StockGroup)
class grpadmin(admin.ModelAdmin):
    list_display = ('id','grp_name')
min


@admin.register(CreateStockCateg)
class CreateStockCategadmin(admin.ModelAdmin):
    list_display = ('id','name','alias','under_name','quantities')    

@admin.register(stock_item)
class stock_itemadmin(admin.ModelAdmin):
    list_display = ('id','name','alias','quantity','rateper','value','group')      

