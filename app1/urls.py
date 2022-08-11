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

    path('catgroupsummary',views.catgroupsummary,name='catgroupsummary'),
     path('groupsummarypage',views.groupsummarypage,name='groupsummarypage'),
    path('creategroups',views.creategroups,name='creategroups'),
    path('primarygrpsummary/<int:sk>',views.primarygrpsummary,name='primarygrpsummary'),
    path('secondarygrpsummary/<int:sk>',views.secondarygrpsummary,name='secondarygrpsummary'),
    path('productsummary/<int:sk>',views.productsummary,name='productsummary'),
    path('prdctmonthlysummary/<int:sk>',views.prdctmonthlysummary,name='prdctmonthlysummary'),
    path('vouchsummary/<int:sk>/<int:m>/<int:n>',views.vouchsummary,name='vouchsummary'),
     path('periodvouchsummary/<int:sk>/<int:m>/<int:n>',views.periodvouchsummary,name='periodvouchsummary'),
    
    path('categorysummary',views.categorysummary,name='categorysummary'),
    path('createcategory',views.createcategory,name='createcategory'),
    path('primarycatsummary/<int:sk>',views.primarycatsummary,name='primarycatsummary'),
    path('secondarycatsummary/<int:sk>',views.secondarycatsummary,name='secondarycatsummary'),
    path('prcatsummary/<int:sk>',views.prcatsummary,name='prcatsummary'),
    path('productcatmonthlysummary/<int:sk>',views.productcatmonthlysummary,name='productcatmonthlysummary'),

    path('savestockgroup',views.savestockgroup,name='savestockgroup'),
    path('savestockcategory',views.savestockcategory,name='savestockcategory'),

    

]