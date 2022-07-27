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
    path('primarygroups',views.primarygroups,name='primarygroups'),
    path('groupsummarypage',views.groupsummarypage,name='groupsummarypage'),
    path('secondarysummary',views.secondarysummary,name='secondarysummary'),
    path('productsummary',views.productsummary,name='productsummary'),
    path('vouchersummary',views.vouchersummary,name='vouchersummary'),
    
    path('categorysummary',views.categorysummary,name='categorysummary'),
    path('primarycategory',views.primarycategory,name='primarycategory'),
    path('categorysummarypage',views.categorysummarypage,name='categorysummarypage'),
    path('secondarycategory',views.secondarycategory,name='secondarycategory'),
    path('productcategory',views.productcategory,name='productcategory'),
    
]