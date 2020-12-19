from django.shortcuts import render
from .models import *

def dashboard(request):
	args={}
	return render(request, 'view_cntr/dashboard.html', args)

def view_cntr(request):
	products = dailyViewCount.objects.all()
	products = products.order_by('-count')[0:49]
	args = {'products': products}
	return render(request, 'view_cntr/view-cntr.html', args)
