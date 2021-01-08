import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aeki_web.settings')

import django
django.setup()
from django.core.wsgi import get_wsgi_application
from view_cntr.models import *
from django.db.models import Avg

import urllib.request
from time import sleep
import time
import datetime
import ast
import io
import json
import requests

st = time.time()
nw_cntr = 0
print(f'------------ {datetime.datetime.now()} ------------')
def ext_str(val, sis, eis):
	try:
		si = val.index(sis)+len(sis)
		ei = val[si:].index(eis)+si
		return val[si:ei]
	except:
		pass
		# print('Err', val)

def ext_pkg(val, sis, eis):
	try:
		si = val.index(sis)+len(sis)
		ei = val[si:].index(eis)+si
		return float(val[si:ei].split(' ')[0])
	except:
		pass
		# print('Err: ',val)

def extract_url(val, sis, eis):
	si = val.index(sis)
	ei = val.index(eis)
	return val[si+len(sis):ei+1]

def get_man_cats():
	sa = []
	main_cat_url = []
	url = 'https://www.ikea.com/ae/en/'
	f = urllib.request.urlopen(url)
	rep = f.read().decode("utf-8")
	sp = rep.split('\n')
	sis = 'href="'
	eis = '/"'
	for i in sp:
		if '001/' in i:
			cat_url = extract_url(i, sis, eis)
			main_cat_url.append(cat_url)
	print(f'{len(main_cat_url)} main_cat_url extracted')
	return main_cat_url

def get_cats():
	cats = []
	main_cats = get_man_cats()
	sis = 'href="'
	eis = '/"'
	for url in main_cats:
		f = urllib.request.urlopen(url)
		rep = f.read().decode("utf-8")
		sp = rep.split('\n')
		for i in sp:
			if 'vn__nav__link' in i:
				cats.append(extract_url(i, sis, eis))
	print(f'{len(cats)} cats extracted')
	return cats

def get_sub_cats():
	cats = get_cats()
	sub_cats = []
	sis = 'href="'
	eis = '/"'
	for url in cats:
		f = urllib.request.urlopen(url)
		rep = f.read().decode("utf-8")
		sp = rep.split('\n')
		for i in sp:
			if 'vn__nav__link' in i:
				sub_cats.append(extract_url(i, sis, eis))
	print(f'{len(sub_cats)} sub_cats extracted')
	return sub_cats

def check_for_new_products():
	sub_cats = get_sub_cats()
	for idx,val in enumerate(sub_cats):
		# print('val: ',val)
		cat_id = val.split('-')[-1].split('/')[0]
		json_url = f'https://sik.search.blue.cdtapps.com/ae/en/product-list-page?category={cat_id}&size=480'
		# print('json_url:\t',json_url)
		try:
			f = urllib.request.urlopen(json_url)
			rep = str(f.read().decode("utf-8"))
			d=json.loads(rep)
			po=d['productListPage']['productWindow']
			for i in po:
				d={}
				pid = i['id']
				url = i['pipUrl']
				obj, created = Product.objects.update_or_create(
					pid=pid, url=url,
				)
				if created:
					global nw_cntr
					nw_cntr += 1
					# print('New product Added:  ',obj)
				else:
					# print('Product Already exists: ',obj)
					pass
		except:
			pass



def update_product_details():
	check_for_new_products()
	err = []
	products = Product.objects.all()
	nw_prds = 0
	for i,val in enumerate(products):
		print(f'Remaining: {len(products)-i}',i)
		url = val.url
		# print(url)
		try:
			f = urllib.request.urlopen(url)
			rep = str(f.read().decode("utf-8"))
			brand_sis = '<div class="range-revamp-header-section__title--big">'
			brand_eis = '</div>'
			brand = ext_str(val=rep,sis=brand_sis,eis=brand_eis)
			Product.objects.filter(pk=val.pk).update(brand=brand)
			# print('brand:',brand)
		except:
			pass


		try:
			title_sis = '<span class="range-revamp-header-section__description-text">'
			title_eis = '</span>'
			title = ext_str(val=rep,sis=title_sis,eis=title_eis)
			# print('title:',title)
			Product.objects.filter(pk=val.pk).update(title=title)
		except:
			err.append(val)
		
		

		try:
			price_sis = '<span class="range-revamp-price__integer">'
			price_eis = '</span>'
			price = ext_str(val=rep,sis=price_sis,eis=price_eis)
			# print('price:',price)
			Product.objects.filter(pk=val.pk).update(price=price)
		except:
			err.append(val)

		try:
			width_sis = 'class="range-revamp-product-details__label">Width: '
			width_eis = '</span><span class="range-revamp-product-details__label">Height:'
			width = ext_pkg(rep,width_sis,width_eis)
			# print('width:',width)
			Product.objects.filter(pk=val.pk).update(width=width)
		except:
			err.append(val)

		try:
			height_sis = '</span><span class="range-revamp-product-details__label">Height: '
			height_eis = '</span><span class="range-revamp-product-details__label">Length: '
			height = ext_pkg(rep,height_sis,height_eis)
			# print('height:',height)
			Product.objects.filter(pk=val.pk).update(height=height)
		except:
			err.append(val)

		try:
			length_sis = '</span><span class="range-revamp-product-details__label">Length: '
			length_eis = '</span><span class="range-revamp-product-details__label">Weight: '
			length = ext_pkg(rep,length_sis,length_eis)
			# print('length:',length)
			Product.objects.filter(pk=val.pk).update(length=length)
		except:
			err.append(val)

		try:
			weight_sis = '</span><span class="range-revamp-product-details__label">Weight: '
			weight_eis = '</span><span class="range-revamp-product-details__label">Package(s):'
			weight = ext_pkg(rep,weight_sis,weight_eis)
			# print('weight:',weight)
			Product.objects.filter(pk=val.pk).update(weight=weight)
		except:
			err.append(val)

		try:
			delivery_availability_sis = '<span class="range-revamp-stockcheck__text">'
			delivery_availability_eis = '</span>'
			delivery_availability = ext_str(val=rep,sis=delivery_availability_sis,eis=delivery_availability_eis)
			# print('delivery_availability:',delivery_availability)
			Product.objects.filter(pk=val.pk).update(delivery_availability=delivery_availability)
		except:
			err.append(val)	
	print(f'{nw_cntr} new products added.')

def calc_tm():
	nw = datetime.datetime.now()
	et = time.time()
	tt = int((et-st)/60)
	hrs = int(tt/60)
	mins = tt%60
	print(f'Task completed in: {hrs}:{mins}')

update_product_details()
calc_tm()
print(f'------------ {datetime.datetime.now()} ------------')
