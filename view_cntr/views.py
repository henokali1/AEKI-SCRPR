from django.shortcuts import render
from .models import *

def dashboard(request):
	args={}
	if request.method == 'POST':
		try:
			price_min = float(request.POST['price_min'])
		except:
			price_min = 0.0
		try:
			price_max = float(request.POST['price_max'])
		except:
			price_max = 0.0
		try:
			width_max = float(request.POST['width'])
			width_min = 0.0
		except:
			width_max = 100000000.0
			width_min = 0.0
		try:
			height_max = float(request.POST['height'])
			height_min = 0.0
		except:
			height_min = 0.0
			height_max = 100000000.0
		try:
			length_max = float(request.POST['length'])
			length_min = 0.0
		except:
			length_min = 0.0
			length_max = 100000000.0
		try:
			weight_max = float(request.POST['weight'])
			weight_min = 0.0
		except:
			weight_max = 100000000.0
			weight_min = 0.0
		
		sort_by = request.POST['sort_by']
		if sort_by == 'high_to_low':
			srt = '-price'
		if sort_by == 'low_to_high':
			srt = 'price'
		print(sort_by)

		args['price_min'] = price_min
		args['price_max'] = price_max
		args['width'] = width_max
		args['height'] = height_max
		args['length'] = length_max
		args['weight'] = weight_max

		products = Product.objects.filter(
			delivery_availability = 'Available for delivery', price__gte=price_min, price__lte=price_max,
			width__gte=width_min, width__lte=width_max, weight__gte=weight_min, weight__lte=weight_max,
			height__gte=height_min, height__lte=height_max, length__gte=length_min, length__lte=length_max,
		).order_by(srt).exclude(delivery_availability = 'Not available for delivery')
		# products = products.order_by('-count')[0:50]
		products = products[0:50]
		args['products'] = products

	return render(request, 'view_cntr/dashboard.html', args)

def view_cntr(request):
	products = dailyViewCount.objects.all()
	products = products.order_by('-count')[0:50]
	args = {'products': products}
	return render(request, 'view_cntr/view-cntr.html', args)
