from django.urls import path,include
from.import views


urlpatterns = [

    path('',views.base,name='base'),
    path('index',views.index,name='index'),
    path('group',views.group,name='group'),
    path('branch',views.branch,name='branch'),
    path('ledger',views.ledger,name='ledger'),
    path('primary',views.primary,name='primary'),
    path('costcat',views.costcat,name='costcat'),
    path('costcentr',views.costcentr,name='costcentr'),
    path('voucher',views.voucher,name='voucher'),
    path('vouchpage',views.vouchpage,name='vouchpage'),

    path('groupsummary',views.groupsummary,name='groupsummary'),
    path('creategroups',views.creategroups,name='creategroups'),
    path('primarygrpsummary/<int:sk>',views.primarygrpsummary,name='primarygrpsummary'),
    path('secondarygrpsummary/<int:sk>',views.secondarygrpsummary,name='secondarygrpsummary'),
    path('productsummary/<int:sk>',views.productsummary,name='productsummary'),
    path('prdctmonthlysummary/<int:sk>',views.prdctmonthlysummary,name='prdctmonthlysummary'),
    path('vouchsummary/<int:sk>',views.vouchsummary,name='vouchsummary'),
    
    path('categorysummary',views.categorysummary,name='categorysummary'),
    path('primarycategory',views.primarycategory,name='primarycategory'),
    path('categorysummarypage',views.categorysummarypage,name='categorysummarypage'),
    path('secondarycategory',views.secondarycategory,name='secondarycategory'),
    path('productcategory',views.productcategory,name='productcategory'),
    


    path('savestockgroup',views.savestockgroup,name='savestockgroup'),
]