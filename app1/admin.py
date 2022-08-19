from django.contrib import admin
from app1.models import CreateStockGrp,CreateStockCateg, StockGroup, Stockcategory, createaccountingGroups,stock_item,voucherlist,company,accountingGroups,ledger
# Register your models here.
@admin.register(CreateStockGrp)
class stockgrpadmin(admin.ModelAdmin):
    list_display = ('id','name','alias','under','quantities','group')

@admin.register(StockGroup)
class grpadmin(admin.ModelAdmin):
    list_display = ('id','grp_name')

@admin.register(Stockcategory)
class catadmin(admin.ModelAdmin):
    list_display = ('id','cat_name')

@admin.register(CreateStockCateg)
class CreateStockCategadmin(admin.ModelAdmin):
    list_display = ('id','name','alias','under','quantities','category')    

@admin.register(stock_item)
class stock_itemadmin(admin.ModelAdmin):
    list_display = ('id','name','alias','quantity','rateper','value','group','category')      

@admin.register(voucherlist)
class voucheradmin(admin.ModelAdmin):
    list_display = ('id','item','party_name','vouch_type','date','quantity','rateper','value','group','category')

@admin.register(company)
class companyadmin(admin.ModelAdmin):
    list_display = ('id','comp_name','start_date')   

@admin.register(accountingGroups)
class accountingGroupsadmin(admin.ModelAdmin):
    list_display = ('id','builtgrp_name') 


@admin.register(createaccountingGroups)
class createaccountingGroupsadmin(admin.ModelAdmin):
    list_display = ('id','usergrp_name','under') 

@admin.register(ledger)
class ledgeradmin(admin.ModelAdmin):
    list_display = ('id','name','alias','under')     