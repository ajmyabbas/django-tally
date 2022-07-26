from django.shortcuts import render

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
    return render(request, 'groupsummary.html')

def categorysummary(request):
    return render(request, 'categorysummary.html')

def primarygroups(request):
    return render(request, 'primarygroups.html')

def primarycategory(request):
    return render(request, 'primarycategory.html')

def groupsummarypage(request):
    return render(request, 'groupsummarypage.html')            

def productsummary(request):
    return render(request, 'productsummary.html')

