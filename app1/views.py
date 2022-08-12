from datetime import date
from errno import ETIME
from re import S
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
    l=[]
    i=0
    h=0
    for c in cat:
      cc=Stockcategory.objects.get(cat_name=c.name)
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
      c.q=ttpq-ttsq 
      c.i=a
      h=h+c.i
      c.y=y
      i=i+1 
    con={
        'cat':cat,'a':a,'y':y,'l':l,'h':h
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
    ia=a
    ib=b
    oc=c
    od=d
    a=a+qty
    b=b+val
    aa=a-c
    

    e=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    f=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    g=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    h=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    ie=e
    iv=f
    og=g
    oh=h
    cc=e-g
    cb5=aa+cc
    

    i=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    j=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    k=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    l=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    iiq=i
    ij=j
    okq=k
    ol=l
    ee=i-k
    cb6=cb5+ee
     
    
    m=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    n=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    o=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    p=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    im=m
    inv=n
    ooq=o
    op=p
    gg=m-o
    cb7=cb6+gg

    q=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    r=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    s=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    t=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    iq=q
    ir=r
    os=s
    ot=t
    ii=q-s
    cb8=cb7+ii

    u=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    v=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    w=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    x=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    iu=u
    ivv=v
    ow=w
    ox=x
    kk=u-w
    cb9=cb8+kk
    
    y=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    z=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    a1=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    b1=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    iy=y
    iz=z
    oa1=a1
    ob1=b1 
    mm=y-a1
    cb10=cb9+mm

    c1=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    d1=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    e1=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    f1=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    ic1=c1
    id1=d1
    oe1=e1
    of1=f1
    oo=c1-e1
    cb11=cb10+oo

    g1=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    h1=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    i1=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    j1=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    ig1=g1
    ih1=h1
    oi1=i1
    oj1=j1
    qq=g1-i1
    cb12=cb11+qq

    k1=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    l1=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    m1=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    n1=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    ik1=k1
    il1=l1
    om1=m1
    on1=n1
    ss=k1-m1
    cb1=cb12+ss

    o1=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    p1=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    q1=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    r1=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
    io1=o1
    ip1=p1
    oq1=q1
    or1=r1
    uu=o1-q1
    cb2=cb1+uu

    s1=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    t1=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
    u1=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
    v1=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']                            
    is1=s1
    it1=t1
    ou1=u1
    ov1=v1
    ww=s1-u1
    cb3=cb2+ww
    
    
    
    
    
    
    
    
    con={
        'si':si,
        'a':a,'b':b,'c':c,'d':d,'e':e,'f':f,'g':g,'h':h,'i':i,'j':j,'k':k,'l':l,'m':m,'n':n,'o':o,'p':p,'q':q,'r':r,'s':s,'t':t,'u':u,'v':v,'w':w,'x':x,'y':y,'z':z ,'a1':a1,
        'b1':b1,'c1':c1,'d1':d1,'e1':e1,'f1':f1,'g1':g1,'h1':h1,'i1':i1,'j1':j1,'k1':k1,'l1':l1,'m1':m1,'n1':n1,'o1':o1,'p1':p1,'q1':q1,'r1':r1,'s1':s1,'t1':t1,'u1':u1,'v1':v1,
        
        'ia':ia,'ib':ib,'oc':oc,'od':od,'ie':ie,'iv':iv,'og':og,'oh':oh,'iiq':iiq,'ij':ij,'okq':okq,'ol':ol,'im':im,'inv':inv,'ooq':ooq,'op':op,'iq':iq,'ir':ir,'os':os,'ot':ot,'iu':iu,'ivv':ivv,'ow':ow,'ox':ox,'iy':iy,'iz':iz ,'oa1':oa1,
        'ob1':ob1,'ic1':ic1,'id1':id1,'oe1':oe1,'of1':of1,'ig1':ig1,'ih1':ih1,'oi1':oi1,'oj1':oj1,'ik1':ik1,'il1':il1,'om1':om1,'on1':on1,'io1':io1,'ip1':ip1,'oq1':oq1,'or1':or1,'is1':is1,'it1':it1,'ou1':ou1,'ov1':ov1,
        
        'aa':aa,'cc':cc,'ee':ee,'gg':gg,'ii':ii,'kk':kk,'mm':mm,'oo':oo,'qq':qq,'ss':ss,'uu':uu,'ww':ww,
        'tpq':tpq,'tsq':tsq,'tpv':tpv,'tsv':tsv,'ttq':ttq,'rate':rate
        ,'qty':qty,'val':val,'cb5':cb5,'cb6':cb6,'cb7':cb7,'cb8':cb8,'cb9':cb9,'cb10':cb10,'cb11':cb11,'cb12':cb12,'cb1':cb1,'cb2':cb2,'cb3':cb3,}
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
        ,'qty':qty,'val':val,}
    return render(request, 'prdctmonthlysummary.html',con)
   




def vouchsummary(request,sk,m,n):
    si=stock_item.objects.get(id=sk)
    rate=si.rateper
    
    
    if m==4:
        qty=si.quantity
        val=si.value
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte='2022-04-30')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte='2022-04-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        a=a+qty
        b=b+val
        e=a-c
        f=rate
        tq=e
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==5:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte='2022-05-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==6:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte='2022-06-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        a=a
        b=b
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==7:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte='2022-07-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==8:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte='2022-08-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==9:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte='2022-09-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==10:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte='2022-10-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==11:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte='2022-11-30',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==12:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte='2022-12-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==1:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte='2022-01-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==2:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte='2022-02-28',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==3:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31')
        a=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte='2022-03-31',vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
                                   
    
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
        'fr':fr ,'tq':tq ,'n':n,
        'si':si   
        }
    return render(request, 'vouchersummary.html',con)




def periodvouchsummary(request,sk,m,n):
    si=stock_item.objects.get(id=sk)
    rate=si.rateper
    st=request.POST.get('start')
    et=request.POST.get('end')
    
    if m==4:
        qty=si.quantity
        val=si.value
        v=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et)
        a=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        a=a+qty
        b=b+val
        e=a-c
        f=rate
        tq=e
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-04-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==5:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et)
        a=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-05-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==6:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et)
        a=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        a=a
        b=b
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-06-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==7:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et)
        a=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-07-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==8:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et)
        a=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-08-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==9:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et)
        a=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-09-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==10:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et)
        a=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-10-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==11:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et)
        a=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-11-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==12:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et)
        a=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-12-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==1:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et)
        a=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-01-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==2:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et)
        a=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-02-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
            
    if m==3:
        qty=n
        val=qty*rate
        v=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et)
        a=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        b=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='purchase').aggregate(value=Coalesce(Sum('value'),0))['value']
        c=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        d=voucherlist.objects.filter(item_id=sk,date__gte=st,date__lte=et,vouch_type='sale').aggregate(value=Coalesce(Sum('value'),0))['value']
        e=a-c
        f=rate
        a=a+n
        b=b+(n*f)
        tq=e+n
        fr=tq*f
        for vi in v:
            ed=vi.date
            pur_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte=ed,vouch_type='purchase').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            sale_qty=voucherlist.objects.filter(item_id=sk,date__gte='2022-03-01',date__lte=ed,vouch_type='sale').aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
            vi.cbalance=qty+(pur_qty-sale_qty)
            vi.cvalue=vi.cbalance*rate
                                   
    
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
        'fr':fr ,'tq':tq ,'n':n,
        'si':si   
        }
    return render(request, 'periodvouchersummary.html',con)













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