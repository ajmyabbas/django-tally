from django.shortcuts import render
from app1.models import CreateStockGrp

# Create your views here.

def base(request):
    return render(request, 'base.html')

def index(request):
    return render(request, 'home.html')

def group(request):
    return render(request, 'groups.html')

def branch(request):
    return render(request, 'branch.html')

def ledger(request):
    return render(request, 'ledger.html')

def primary(request):
    return render(request, 'primarycost.html')

def costcat(request):
    return render(request, 'costcat.html')

def costcentr(request):
    return render(request, 'costcentr.html')

def voucher(request):
    return render(request, 'voucher.html')

def vouchpage(request):
    return render(request, 'vouchpage.html')





def savestockgroup(request):
    if request.method=='POST':
        gpname=request.POST['name']
        abr=request.POST['alias']
        undr=request.POST['under']
        q=request.POST.get('qty')
        sg=CreateStockGrp(name=gpname,alias=abr,under_name=undr,quantities=q)
        sg.save()
        gps=CreateStockGrp.objects.all()
        con={
        'gps':gps,
        } 
        return render(request,'groupsummary.html',con)


def groupsummary(request):
    gps=CreateStockGrp.objects.all()
    con={
        'gps':gps,
        } 
    return render(request,'groupsummary.html',con)
   

def categorysummary(request):
    return render(request, 'categorysummary.html')

def primarygroups(request):
    gps=CreateStockGrp.objects.all()
    con={
        'gps':gps,
        } 
    return render(request, 'primarygroups.html',con)

def primarycategory(request):
    return render(request, 'primarycategory.html')

def groupsummarypage(request):
    return render(request, 'groupsummarypage.html')  

def secondarysummary(request):
    return render(request, 'secondarysummarypage.html')              

def productsummary(request):
    return render(request, 'productsummary.html')

def vouchersummary(request):
    return render(request, 'vouchersummary.html')

def categorysummarypage(request):
    return render(request, 'categorysummarypage.html')

def secondarycategory(request):
    return render(request, 'secondarycategorypage.html')

def productcategory(request):
    return render(request, 'productcategory.html')