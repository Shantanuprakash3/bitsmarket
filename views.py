'''
Created on Jul 5, 2014

@author: Arjun
'''
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.http.response import HttpResponse, HttpResponseRedirect,\
    HttpResponseForbidden
from django.contrib import auth
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from UserApp.forms import SignUpForm, ProductForm, EditForm  # @UnresolvedImport
from UserApp import models


def main_view(request):
    t = get_template('mainPage.html')
    products = models.Product.objects.all()
    c = RequestContext(request,{'products':products})
    return HttpResponse(t.render(c))

def signup_view(request):
    if request.user:
        if request.user.is_authenticated():
            return HttpResponse("Logout first and then signup.")
    form = SignUpForm()
    if request.POST:
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("../../loggedin")
        else:
            c = Context({'form':form})
            return render_to_response('signUp.html', context_instance=RequestContext(request,c))
    
    c = Context({'form':form})
    return render_to_response('signUp.html', context_instance=RequestContext(request,c))

def login_view(request):
    if not request.user.is_authenticated() :
        errors = ""
        if request.POST:
            userid = request.POST.get('userid','')
            password = request.POST.get('password','')
            user = auth.authenticate(username=userid, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                if request.GET:
                    return HttpResponseRedirect( request.GET['next'])
                return HttpResponseRedirect("../loggedin/")
            else:
                errors = "Invalid Username or Password"
                return render_to_response('login.html', context_instance=RequestContext(request,{'errors':errors}))
        else:
            return render_to_response('login.html', context_instance=RequestContext(request,{'errors':errors}))
        
    else:  
        return HttpResponseRedirect("../loggedin/")

@login_required   
def logged_in_view(request):
    #t = get_template('loggedInTemplate.html')
    #c = RequestContext(request,{'user':request.user })
    return HttpResponseRedirect("../../../../../../../user/products")
    

@login_required
def view_self(request):  
    t = get_template('viewSelf.html')
    c = Context({'user':request.user,'userprofile':request.user.get_profile()})
    return HttpResponse(t.render(c))
    
    
    
@login_required
def edit_self(request):   

    form = EditForm(instance = request.user.get_profile() , initial = {'first_name': request.user.first_name , 'last_name': request.user.last_name })
    if request.POST:
        form = EditForm(instance = request.user.get_profile() ,  data = request.POST, files = request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("../../viewSelf/")
        else:
            c = Context({'form':form})
            return render_to_response('signUp.html', context_instance=RequestContext(request,c))
    
    c = Context({'form':form})
    return render_to_response('signUp.html', context_instance=RequestContext(request,c))
    
@login_required
def product_uploader(request):
    if request.POST:
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            record = form.save(user = request.user)
            return HttpResponseRedirect("../../../../../../../user/products" )
        else:
            c = Context({'form':form})
            return render_to_response('productUploads.html', context_instance=RequestContext(request,c)) 
    else:
        form =  ProductForm()
        c = Context({'form':form})
        return render_to_response('productUploads.html', context_instance=RequestContext(request,c)) 
    


@login_required    
def view_user_products(request):
    user = request.user
    products = models.Product.objects.filter(user = user)
    t = get_template('userProductList.html')
    c = RequestContext(request,{'products':products})
    return HttpResponse(t.render(c))

def sell(request):
    if not request.user.is_authenticated() :
        errors = ""
        if request.POST:
            userid = request.POST.get('userid','')
            password = request.POST.get('password','')
            user = auth.authenticate(username=userid, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                if request.GET:
                    return HttpResponseRedirect( request.GET['next'])
                return HttpResponseRedirect("../loggedin/")
            else:
                errors = "Invalid Username or Password"
                return render_to_response('login.html', context_instance=RequestContext(request,{'errors':errors,'sell':True}))
        else:
            return render_to_response('login.html', context_instance=RequestContext(request,{'errors':errors,'sell':True}))
        
    else:  
        return HttpResponseRedirect("../loggedin/")


def view_product(request):
    try:
        prodid = request.GET.get('id','')
        product = models.Product.objects.get(id = prodid)
        userprof = product.user.userprofile
        t = get_template("productView.html")
        c = RequestContext(request,{'userprofile':userprof ,'user':request.user,'product':product})
        return HttpResponse(t.render(c))
    except:
        return HttpResponse("Something Went wrong, if this persists contact us at 77777777")


@login_required     
def remove_product(request):
    user = request.user
    try:
        prodid = request.GET.get('id','')
        product = models.Product.objects.get(id = prodid)
        if user == product.user:
            product.delete()
            return HttpResponseRedirect("../../../../../../../user/products")
        else:
            return HttpResponseForbidden("You dont have the permission to do this")
    except:
        return HttpResponse("Something Went Wrong Please Try Again.")


@login_required     
def logout(request):
    auth.logout(request) 
    return HttpResponseRedirect("../../login")   
    

