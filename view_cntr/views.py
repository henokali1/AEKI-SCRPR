from django.shortcuts import render
from .models import *

def dashboard(request):
	args={}
	if request.method == 'POST':
		price_min = request.POST['price_min']
		price_max = request.POST['price_max']
		width = request.POST['width']
		height = request.POST['height']
		length = request.POST['length']
		weight = request.POST['weight']

		args['price_min'] = price_min
		args['price_max'] = price_max
		args['width'] = width
		args['height'] = height
		args['length'] = length
		args['weight'] = weight

		products = Product.objects.all()
		# products = products.order_by('-count')[0:50]
		products = products[0:50]
		args['products'] = products

	return render(request, 'view_cntr/dashboard.html', args)

def view_cntr(request):
	products = dailyViewCount.objects.all()
	products = products.order_by('-count')[0:50]
	args = {'products': products}
	return render(request, 'view_cntr/view-cntr.html', args)
