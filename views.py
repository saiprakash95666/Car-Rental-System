from Portal.modules.login.login import *
from Portal.modules.staff.staff import *
from Portal.modules.searchcars.searchcars import *
from Portal.modules.mycarlist.mycarlist import *
from Portal.modules.favbooklist.favbooklist import *
from Portal.modules.cardata.cardata import *
from Portal.modules.addcar.addcar import *

#from django.conf.urls import url
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from requests import api
from django.contrib import auth
# Create your views here.
def Index(request):
    return render(request,'base.html')
def Logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
