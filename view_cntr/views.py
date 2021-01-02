from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
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
			price_max = 100000000.0
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
		fav = request.POST['fav']
		# srt = '-price' if sort_by == 'high_to_low' else 'price'
		if sort_by == 'high_to_low':
			srt = '-price'
		if sort_by == 'low_to_high':
			srt = 'price'
		if sort_by == 'avg_daily_view':
			srt = '-avg_view'
		args['price_min'] = price_min
		args['price_max'] = price_max
		args['width'] = width_max
		args['height'] = height_max
		args['length'] = length_max
		args['weight'] = weight_max
		args['srt'] = srt

		args['is_fav'] = fav
		
		if fav == 'only_fav':
			products = Product.objects.filter(
				is_fav=True, delivery_availability = 'Available for delivery', price__gte=price_min, price__lte=price_max,
				width__gte=width_min, width__lte=width_max, weight__gte=weight_min, weight__lte=weight_max,
				height__gte=height_min, height__lte=height_max, length__gte=length_min, length__lte=length_max,
			).order_by(srt).exclude(delivery_availability = 'Not available for delivery')
		elif fav == 'upc':
			products = Product.objects.filter(
				delivery_availability = 'Available for delivery', price__gte=price_min, price__lte=price_max,
				width__gte=width_min, width__lte=width_max, weight__gte=weight_min, weight__lte=weight_max,
				height__gte=height_min, height__lte=height_max, length__gte=length_min, length__lte=length_max,
			).order_by(srt).exclude(upc='')
		else:
			products = Product.objects.filter(
				delivery_availability = 'Available for delivery', price__gte=price_min, price__lte=price_max,
				width__gte=width_min, width__lte=width_max, weight__gte=weight_min, weight__lte=weight_max,
				height__gte=height_min, height__lte=height_max, length__gte=length_min, length__lte=length_max,
			).order_by(srt).exclude(delivery_availability = 'Not available for delivery')

		page = request.GET.get('page', 1)
		paginator = Paginator(products, 500)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)
		args['products'] = products

	return render(request, 'view_cntr/dashboard.html', args)

def view_cntr(request):
	products = dailyViewCount.objects.all()
	products = products.order_by('-count')[0:50]
	args = {'products': products}
	return render(request, 'view_cntr/view-cntr.html', args)

def fav(request, pk, is_fav):
	val = True if (is_fav == 'True') else False
	Product.objects.filter(pk=pk).update(is_fav=val)
	return JsonResponse({'is_fav':str(val),'pk':pk})

def listed(request, pk, is_listed):
	val = True if (is_listed == 'True') else False
	print('listed: ', val)
	Product.objects.filter(pk=pk).update(is_listed=val)
	return JsonResponse({'is_listed':str(val),'pk':pk})

def daily_view(request, pk):
	args = {'views': dailyViewCount.objects.filter(product=pk)}
	return render(request, 'view_cntr/daily_view.html', args)

def has_upc(request):
	p=Product.objects.exclude(upc='').order_by('-avg_view')
	args = {'products':p}
	return render(request, 'view_cntr/has_upc.html', args)

def test(request):
	args={}
	if request.method == 'POST':
		try:
			price_min = float(request.POST['price_min'])
		except:
			price_min = 0.0
		try:
			price_max = float(request.POST['price_max'])
		except:
			price_max = 100000000.0
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
		# fav = request.POST['fav']

		if sort_by == 'high_to_low':
			srt = '-price'
		if sort_by == 'low_to_high':
			srt = 'price'
		if sort_by == 'avg_daily_view':
			srt = '-avg_view'
		args['price_min'] = price_min
		args['price_max'] = price_max
		args['width'] = width_max
		args['height'] = height_max
		args['length'] = length_max
		args['weight'] = weight_max
		args['srt'] = srt

		# args['is_fav'] = fav
		
		# if fav == 'only_fav':
		# 	products = Product.objects.filter(
		# 		is_fav=True, delivery_availability = 'Available for delivery', price__gte=price_min, price__lte=price_max,
		# 		width__gte=width_min, width__lte=width_max, weight__gte=weight_min, weight__lte=weight_max,
		# 		height__gte=height_min, height__lte=height_max, length__gte=length_min, length__lte=length_max,
		# 	).order_by(srt).exclude(delivery_availability = 'Not available for delivery')
		# elif fav == 'upc':
		# 	products = Product.objects.filter(
		# 		delivery_availability = 'Available for delivery', price__gte=price_min, price__lte=price_max,
		# 		width__gte=width_min, width__lte=width_max, weight__gte=weight_min, weight__lte=weight_max,
		# 		height__gte=height_min, height__lte=height_max, length__gte=length_min, length__lte=length_max,
		# 	).order_by(srt).exclude(upc='')
		# else:
		# 	products = Product.objects.filter(
		# 		delivery_availability = 'Available for delivery', price__gte=price_min, price__lte=price_max,
		# 		width__gte=width_min, width__lte=width_max, weight__gte=weight_min, weight__lte=weight_max,
		# 		height__gte=height_min, height__lte=height_max, length__gte=length_min, length__lte=length_max,
		# 	).order_by(srt).exclude(delivery_availability = 'Not available for delivery')

		include = request.POST.getlist('include')
		print('include', include)

		products = Product.objects.all()

		if 'fav' in include:
			products = products.filter(is_fav=True)
			args['is_fav'] = True
		if 'upc' in include:
			products = products.exclude(upc='')
			args['upc'] = True
		if 'listed' in include:
			products = products.filter(is_listed=True)
			args['listed'] = True
		if 'all' in include:
			args['all'] = True

		page = request.GET.get('page', 1)
		paginator = Paginator(products, 500)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)
		args['products'] = products

	return render(request, 'view_cntr/test.html', args)
