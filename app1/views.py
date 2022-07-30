from django.shortcuts import redirect, render
from app1.models import CreateStockGrp, StockGroup, stock_item

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




def groupsummary(request):
    gps=StockGroup.objects.all()
    con={
        'gps':gps,
        } 
    return render(request,'groupsummary.html',con)

def creategroups(request):
    gps=StockGroup.objects.all()
    con={
        'gps':gps,
        } 
    return render(request, 'creategroup.html',con)    

def savestockgroup(request):
    if request.method=='POST':
        gpname=request.POST['name']
        s=StockGroup(grp_name=gpname)
        s.save()
        abr=request.POST['alias']
        grp=request.POST.get('u')
        gp=StockGroup.objects.get(grp_name=grp)
        q=request.POST.get('qty')
        sg=CreateStockGrp(name=gpname,alias=abr,quantities=q,group=gp)
        sg.save()
        return redirect('groupsummary')




def primarygrpsummary(request,sk):
    gps=CreateStockGrp.objects.filter(group_id=sk)
    con={
        'gps':gps,
        'sk':sk,
        } 
    return render(request, 'primarygrpsummary.html',con)  

def secondarygrpsummary(request,sk):
    gps=StockGroup.objects.filter(id=sk)
    
    con={
        'gps':gps,
        } 
    return render(request, 'secondarygrpsummary.html',con)  
def productsummary(request):
    return render(request, 'productsummary.html')

def prdctmonthlysummary (request):
    return render(request, 'prdctmonthlysummary.html')
   

def vouchersummary(request):
    return render(request, 'vouchersummary.html')
















def categorysummary(request):
    return render(request, 'categorysummary.html')


def primarycategory(request):
    return render(request, 'primarycategory.html')
def categorysummarypage(request):
    return render(request, 'categorysummarypage.html')

def secondarycategory(request):
    return render(request, 'secondarycategorypage.html')

def productcategory(request):
    return render(request, 'productcategory.html')