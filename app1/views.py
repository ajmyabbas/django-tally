from unittest import signals
from webbrowser import get
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, render
from app1 import models
from app1.models import CreateStockCateg, CreateStockGrp, StockGroup, Stockcategory, stock_item,voucherlist
from django.db.models import Sum

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

def groupsummarypage(request):
    gps=CreateStockGrp.objects.all()
    con={
        'gps':gps,
        } 
    return render(request,'groupsummarypage.html',con)


def catgroupsummary(request):
    cat=CreateStockCateg.objects.all()
    con={
        'cat':cat,
        } 
    return render(request,'catgroupsummary.html',con)

def categorysummary(request):
    gps=CreateStockGrp.objects.all()
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

def createcategory(request):
    cat=Stockcategory.objects.all()
    con={
        'cat':cat,
        } 
    return render(request, 'createcategory.html',con) 

def savestockgroup(request):
    if request.method=='POST':
        gpname=request.POST['name']
        s=StockGroup(grp_name=gpname)
        s.save()
        abr=request.POST['alias']
        grp=request.POST.get('u')
        gp=StockGroup.objects.get(grp_name=grp)
        q=request.POST.get('qty')
        sg=CreateStockGrp(name=gpname,alias=abr,quantities=q,under=grp,group=gp)
        sg.save()
        return redirect('groupsummarypage')

def savestockcategory(request):
    if request.method=='POST':
        catname=request.POST['name']
        s=Stockcategory(cat_name=catname)
        s.save()
        abr=request.POST['alias']
        cat=request.POST.get('u')
        c=Stockcategory.objects.get(cat_name=cat)
        q=request.POST.get('qty')
        sc=CreateStockCateg(name=catname,alias=abr,quantities=q,under=cat,category=c)
        sc.save()
        return redirect('catgroupsummary')


def primarygrpsummary(request,sk):
    gps=CreateStockGrp.objects.filter(group_id=sk)
    gt=0
    for g in gps:
        gg=StockGroup.objects.get(grp_name=g.name)
        gpsi= CreateStockGrp.objects.filter(group_id=gg.id)
        l=[]
        i=0
        h=0
        for gi in gpsi:
           gg=StockGroup.objects.get(grp_name=gi.name)
           si=stock_item.objects.filter(group_id=gg.id)
           ttpq=0
           ttsq=0
           r=0
           a=0
           y=0
      
           for s in si:
               w=s.rateper 
               oqty=s.quantity
               val=s.value
               tpq=voucherlist.objects.filter(item_id=s.id,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
               tpq=tpq+oqty
               ttpq=tpq+ttpq
               tsq=voucherlist.objects.filter(item_id=s.id,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
               ttsq=tsq+ttsq
               ttq=tpq-tsq
               s.qy=ttq
               s.value=ttq * w
               a=a+s.value
               y=y+w
           gi.q=ttpq-ttsq 
           gi.i=a
           h=h+gi.i
           gi.y=y
           i=i+1 
           gi.h=h   
           g.h=h
        gt=gt+g.h   
            



    con={
        'gpsi':gpsi,
        'gps':gps,
        'sk':sk,
        'gt':gt
        } 
    return render(request, 'primarygrpsummary.html',con)  

def primarycatsummary(request,sk):
    cat=CreateStockCateg.objects.filter(category_id=sk)
    gt=0
    for c in cat:
        cc=Stockcategory.objects.get(cat_name=c.name)
        cgsi= CreateStockCateg.objects.filter(category_id=cc.id)
        l=[]
        i=0
        h=0
        for ci in cgsi:
           cc=Stockcategory.objects.get(cat_name=ci.name)
           si=stock_item.objects.filter(category_id=cc.id)
           ttpq=0
           ttsq=0
           r=0
           a=0
           y=0
      
           for s in si:
               w=s.rateper 
               oqty=s.quantity
               val=s.value
               tpq=voucherlist.objects.filter(item_id=s.id,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
               tpq=tpq+oqty
               ttpq=tpq+ttpq
               tsq=voucherlist.objects.filter(item_id=s.id,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
               ttsq=tsq+ttsq
               ttq=tpq-tsq
               s.qy=ttq
               s.value=ttq * w
               a=a+s.value
               y=y+w
           ci.q=ttpq-ttsq 
           ci.i=a
           h=h+ci.i
           ci.y=y
           i=i+1 
           ci.h=h   
           c.h=h
        gt=gt+c.h   
            



    con={
        'cgsi':cgsi,
        'cat':cat,
        'sk':sk,
        'gt':gt
        } 
    return render(request, 'primarycatsummary.html',con)

def secondarygrpsummary(request,sk):
    gps=CreateStockGrp.objects.get(id=sk)
    gg=StockGroup.objects.get(grp_name=gps.name)
    gps= CreateStockGrp.objects.filter(group_id=gg.id)
    l=[]
    i=0
    h=0
    for g in gps:
      gg=StockGroup.objects.get(grp_name=g.name)
      si=stock_item.objects.filter(group_id=gg.id)
      ttpq=0
      ttsq=0
      r=0
      a=0
      y=0
      
      for s in si:
            w=s.rateper 
            oqty=s.quantity
            val=s.value
            tpq=voucherlist.objects.filter(item_id=s.id,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            tpq=tpq+oqty
            ttpq=tpq+ttpq
            tsq=voucherlist.objects.filter(item_id=s.id,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            ttsq=tsq+ttsq
            ttq=tpq-tsq
            s.qy=ttq
            s.value=ttq * w
            a=a+s.value
            y=y+w
      g.q=ttpq-ttsq 
      g.i=a
      h=h+g.i
      g.y=y
      i=i+1 
    con={
        'gps':gps,'a':a,'y':y,'gps':gps,'l':l,'h':h
        } 
    return render(request, 'secondarygrpsummary.html',con) 

def secondarycatsummary(request,sk):
    cat=CreateStockCateg.objects.get(id=sk)
    cc=Stockcategory.objects.get(cat_name=cat.name)
    cat= CreateStockCateg.objects.filter(category_id=cc.id)
    con={
        'cat':cat,
        } 
    return render(request, 'secondarycatsummary.html',con)    

def productsummary(request,sk):
    gps=CreateStockGrp.objects.get(id=sk)
    gg=StockGroup.objects.get(grp_name=gps.name)
    si=stock_item.objects.filter(group_id=gg.id)
    ttpq=0
    ttsq=0
    r=0
    a=0
    y=0
    for s in si:
        w=s.rateper
        qty=s.quantity
        val=s.value
        tpq=voucherlist.objects.filter(item_id=s.id,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        tpq=tpq+qty
        ttpq=tpq+ttpq
        tsq=voucherlist.objects.filter(item_id=s.id,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        ttsq=tsq+ttsq
        ttq=tpq-tsq
        s.qy=ttq
        s.value=ttq * w
        a=a+s.value
        y=y+w
    
    
    q=ttpq-ttsq   
    con={
        'si':si,'ttpq':ttpq,'q':q,'ttpq':ttq,'w':w,'a':a,'y':y
        } 
    return render(request, 'productsummary.html',con)


def prcatsummary(request,sk):
    cat=CreateStockCateg.objects.get(id=sk)
    cc=Stockcategory.objects.get(cat_name=cat.name)
    si=stock_item.objects.filter(category_id=cc.id)
    ttpq=0
    ttsq=0
    r=0
    a=0
    y=0
    for s in si:
        w=s.rateper
        qty=s.quantity
        val=s.value
        tpq=voucherlist.objects.filter(item_id=s.id,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        tpq=tpq+qty
        ttpq=tpq+ttpq
        tsq=voucherlist.objects.filter(item_id=s.id,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        ttsq=tsq+ttsq
        ttq=tpq-tsq
        s.qy=ttq
        s.value=ttq * w
        a=a+s.value
        y=y+w
    
    
    q=ttpq-ttsq   
    con={
        'si':si,'ttpq':ttpq,'q':q,'ttpq':ttq,'w':w,'a':a,'y':y
        } 
    return render(request, 'productcatsummary.html',con) 

def prdctmonthlysummary(request,sk):
    si=stock_item.objects.get(id=sk)
    rate=si.rateper
    qty=si.quantity
    val=si.value
    tpq=voucherlist.objects.filter(item_id=si.id,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    tpq=tpq+qty
    tpv=voucherlist.objects.filter(item_id=si.id,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    tpv=tpv+val
    tsq=voucherlist.objects.filter(item_id=si.id,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    tsv=voucherlist.objects.filter(item_id=si.id,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    ttq=tpq-tsq
    rate=si.rateper
    qty=si.quantity
    val=si.value
    
    a=voucherlist.objects.filter(item_id=si.id,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    b=voucherlist.objects.filter(item_id=si.id,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    c=voucherlist.objects.filter(item_id=si.id,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    d=voucherlist.objects.filter(item_id=si.id,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    a=a+qty
    b=b+val
    aa=a-c
    

    e=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    f=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    g=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    h=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    cc=e-g
    

    i=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    j=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    k=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    l=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    ee=i-k
   
     
    
    m=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    n=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    o=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    p=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    gg=m-o
    

    q=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    r=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    s=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    t=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    ii=q-s
    
    u=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    v=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    w=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    x=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    kk=u-w
    
    y=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    z=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    a1=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    b1=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    mm=y-a1
    
    c1=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    d1=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    e1=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    f1=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    oo=c1-e1
    
    g1=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    h1=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    i1=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    j1=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    qq=g1-i1
    
    k1=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    l1=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    m1=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    n1=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    ss=k1-m1
    
    o1=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    p1=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    q1=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    r1=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    uu=o1-q1
    
    s1=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    t1=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    u1=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    v1=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']                            
    ww=s1-u1
    
    
    
    
    
    
    
    
    
    con={
        'si':si,
        'a':a,'b':b,'c':c,'d':d,'e':e,'f':f,'g':g,'h':h,'i':i,'j':j,'k':k,'l':l,'m':m,'n':n,'o':o,'p':p,'q':q,'r':r,'s':s,'t':t,'u':u,'v':v,'w':w,'x':x,'y':y,'z':z ,'a1':a1,
        'b1':b1,'c1':c1,'d1':d1,'e1':e1,'f1':f1,'g1':g1,'h1':h1,'i1':i1,'j1':j1,'k1':k1,'l1':l1,'m1':m1,'n1':n1,'o1':o1,'p1':p1,'q1':q1,'r1':r1,'s1':s1,'t1':t1,'u1':u1,'v1':v1
        
        ,'aa':aa,'cc':cc,'ee':ee,'gg':gg,'ii':ii,'kk':kk,'mm':mm,'oo':oo,'qq':qq,'ss':ss,'uu':uu,'ww':ww,
        'tpq':tpq,'tsq':tsq,'tpv':tpv,'tsv':tsv,'ttq':ttq,'rate':rate
        ,'qty':qty,'val':val}
    return render(request, 'prdctmonthlysummary.html',con)
   


def productcatmonthlysummary(request,sk):
    si=stock_item.objects.get(id=sk)
    rate=si.rateper
    qty=si.quantity
    val=si.value
    tpq=voucherlist.objects.filter(item_id=si.id,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    tpq=tpq+qty
    tpv=voucherlist.objects.filter(item_id=si.id,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    tpv=tpv+val
    tsq=voucherlist.objects.filter(item_id=si.id,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    tsv=voucherlist.objects.filter(item_id=si.id,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    ttq=tpq-tsq
    rate=si.rateper
    qty=si.quantity
    val=si.value
    
    a=voucherlist.objects.filter(item_id=si.id,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    b=voucherlist.objects.filter(item_id=si.id,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    c=voucherlist.objects.filter(item_id=si.id,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    d=voucherlist.objects.filter(item_id=si.id,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    a=a+qty
    b=b+val
    aa=a-c
    

    e=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    f=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    g=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    h=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    cc=e-g
    

    i=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    j=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    k=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    l=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    ee=i-k
   
     
    
    m=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    n=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    o=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    p=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    gg=m-o
    

    q=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    r=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    s=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    t=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    ii=q-s
    
    u=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    v=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    w=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    x=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    kk=u-w
    
    y=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    z=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    a1=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    b1=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    mm=y-a1
    
    c1=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    d1=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    e1=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    f1=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    oo=c1-e1
    
    g1=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    h1=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    i1=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    j1=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    qq=g1-i1
    
    k1=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    l1=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    m1=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    n1=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    ss=k1-m1
    
    o1=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    p1=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    q1=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    r1=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    uu=o1-q1
    
    s1=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    t1=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    u1=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    v1=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']                            
    ww=s1-u1
    
    
    
    
    
    
    
    
    
    con={
        'si':si,
        'a':a,'b':b,'c':c,'d':d,'e':e,'f':f,'g':g,'h':h,'i':i,'j':j,'k':k,'l':l,'m':m,'n':n,'o':o,'p':p,'q':q,'r':r,'s':s,'t':t,'u':u,'v':v,'w':w,'x':x,'y':y,'z':z ,'a1':a1,
        'b1':b1,'c1':c1,'d1':d1,'e1':e1,'f1':f1,'g1':g1,'h1':h1,'i1':i1,'j1':j1,'k1':k1,'l1':l1,'m1':m1,'n1':n1,'o1':o1,'p1':p1,'q1':q1,'r1':r1,'s1':s1,'t1':t1,'u1':u1,'v1':v1
        
        ,'aa':aa,'cc':cc,'ee':ee,'gg':gg,'ii':ii,'kk':kk,'mm':mm,'oo':oo,'qq':qq,'ss':ss,'uu':uu,'ww':ww,
        'tpq':tpq,'tsq':tsq,'tpv':tpv,'tsv':tsv,'ttq':ttq,'rate':rate
        ,'qty':qty,'val':val}
    return render(request, 'prdctmonthlysummary.html',con)
   




def vouchsummary(request,sk,m):
    si=stock_item.objects.get(id=sk)
    rate=si.rateper
    qty=si.quantity
    val=si.value
    
    if m==4:
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte='2022-04-30')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        a=a+qty
        b=b+val
        e=a-c
        f=rate
        fr=e*f

    if m==5:
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        fr=e*f
    if m==6:
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        a=a
        b=b
        e=a-c
        f=rate
        fr=e*f
    if m==7:
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        fr=e*f
    if m==8:
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        fr=e*f
    if m==9:
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        fr=e*f
    if m==10:
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        fr=e*f
    if m==11:
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        fr=e*f
    if m==12:
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        fr=e*f
    if m==1:
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        fr=e*f
    if m==2:
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        fr=e*f
    if m==3:
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        fr=e*f                        
    
    con={
        'v':v,
        'si':si,
        'm':m,
        'a':a,
        'b':b,
        'c':c,
        'd':d,
        'e':e,
        'f':f,
        'qty':qty,
        'val':val,
        'fr':fr     
        }
    return render(request, 'vouchersummary.html',con)
















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