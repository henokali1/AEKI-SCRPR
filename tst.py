import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aeki_web.settings')

import django
django.setup()
from django.core.wsgi import get_wsgi_application
from view_cntr.models import *
from django.db.models import Avg

import urllib.request
from time import sleep
import pickle
import ast
import io
import json
import requests


def read_pickle_file(fn):
	try:
		with open(fn, 'rb') as handle:
			f = pickle.load(handle)
		return f
	except:
		print(f"Couldn't read {fn}")

def write_pickle_file(fn, val):
	try:
		with open(fn, 'wb') as handle:
			pickle.dump(val, handle, protocol=pickle.HIGHEST_PROTOCOL)
	except:
		print(f"Couldn't write {fn}")

def read_csv_file(fn):
	with open(fn,'r') as f:
		rd = f.read()
	return rd

def write_file(val, file_name='replay.html'):
	try:
		with io.open(file_name, "w", encoding="utf-8") as f:
			f.write(val)
			print(file_name + ' exported')
	except:
		print("Couldn't export data :'(")


def extract_cats():
	for idx,url in enumerate(main_cats):
		f = urllib.request.urlopen(url)
		rep = str(f.read().decode("utf-8"))
		sp = rep.split('\n')
		cntr = 1
		for i in sp:
			if 'https://www.ikea.com/ae/en/cat/' in i:
				try:
					sc = '<a href="'
					ec = '/"'
					si = i.index(sc)+9
					ei = i.index(ec)
					r=i[si:ei]
					if ((r == 'https://www.ikea.com/ae/en/cat/products-products') or (len(r) < 5)):
						pass
					else:
						print(r)
						cats.append(r)
						cntr += 1
				except:
					pass
		print(f'Remaining: {len(main_cats)-idx}')
		sleep(5)
	return(cats)

def extract_sub_cats():
	try:
		sub_cats = []
		for idx,url in enumerate(cats):
			print(url)
			f = urllib.request.urlopen(url)
			rep = str(f.read().decode("utf-8"))
			sp = rep.split('\n')
			cntr = 1
			for i in sp:
				if 'https://www.ikea.com/ae/en/cat/' in i:
					try:
						sc = '<a href="'
						ec = '/"'
						si = i.index(sc)+9
						ei = i.index(ec)
						r=i[si:ei]
						exclude = ['https://www.ikea.com/ae/en/cat/products-products']
						if ((r in exclude) or (len(r) < 5)):
							pass
						else:
							print(r)
							sub_cats.append(r)
							write_file(str(sub_cats))
							cntr += 1
					except:
						pass
			print(f'Remaining: {len(cats)-idx}')
			sleep(2)
		return(sub_cats)
	except:
		pass


def ext_str(val, sis, eis):
	try:
		si = val.index(sis)+len(sis)
		ei = val[si:].index(eis)+si
		return val[si:ei]
	except:
		print('Err', val)

def ext_pkg(val, sis, eis):
	try:
		si = val.index(sis)+len(sis)
		ei = val[si:].index(eis)+si
		return float(val[si:ei].split(' ')[0])
	except:
		print('Err: ',val)

def extract_products_v1():
	for idx,val in enumerate(sub_cats[227:]):
		print(val)
		cat_id = val.split('/')[-1].split('-')[-1]
		json_url = f'https://sik.search.blue.cdtapps.com/ae/en/product-list-page?category={cat_id}&size=480'
		f = urllib.request.urlopen(json_url)
		rep = str(f.read().decode("utf-8"))
		d=json.loads(rep)
		po=d['productListPage']['productWindow']
		print(f'Remainig: {len(sub_cats[227:])-idx}')
		for i in po:
			d={}
			pid = i['id']
			d['id'] = pid
			d['url'] = i['pipUrl']
			od = read_pickle_file('products.pickle')
			od[pid] = d
			write_pickle_file('products.pickle',od)

def extract_product_details():
	for i,val in enumerate(products):
		if i > 6628:
			print(f'Remaining: {len(products)-i}',i)
			print(products[val])
			url = products[val]['url']
			print(url)
			f = urllib.request.urlopen(url)
			rep = str(f.read().decode("utf-8"))

			np = products[val]
			try:
				brand_sis = '<div class="range-revamp-header-section__title--big">'
				brand_eis = '</div>'
				brand = ext_str(val=rep,sis=brand_sis,eis=brand_eis)
				np['brand'] = brand
				print('brand:',brand)
			except:
				err.append(val)


			try:
				title_sis = '<span class="range-revamp-header-section__description-text">'
				title_eis = '</span>'
				title = ext_str(val=rep,sis=title_sis,eis=title_eis)
				np['title'] = title
				print('title:',title)
			except:
				err.append(val)

			try:
				price_sis = '<span class="range-revamp-price__integer">'
				price_eis = '</span>'
				price = ext_str(val=rep,sis=price_sis,eis=price_eis)
				np['price'] = float(price)
				print('price:',price)
			except:
				err.append(val)

			try:
				width_sis = 'class="range-revamp-product-details__label">Width: '
				width_eis = '</span><span class="range-revamp-product-details__label">Height:'
				width = ext_pkg(rep,width_sis,width_eis)
				np['width'] = width
				print('width:',width)
			except:
				err.append(val)

			try:
				height_sis = '</span><span class="range-revamp-product-details__label">Height: '
				height_eis = '</span><span class="range-revamp-product-details__label">Length: '
				height = ext_pkg(rep,height_sis,height_eis)
				np['height'] = height
				print('height:',height)
			except:
				err.append(val)

			try:
				length_sis = '</span><span class="range-revamp-product-details__label">Length: '
				length_eis = '</span><span class="range-revamp-product-details__label">Weight: '
				length = ext_pkg(rep,length_sis,length_eis)
				np['length'] = length
				print('length:',length)
			except:
				err.append(val)

			try:
				weight_sis = '</span><span class="range-revamp-product-details__label">Weight: '
				weight_eis = '</span><span class="range-revamp-product-details__label">Package(s):'
				weight = ext_pkg(rep,weight_sis,weight_eis)
				np['weight'] = weight
				print('weight:',weight)
			except:
				err.append(val)

			try:
				delivery_availability_sis = '<span class="range-revamp-stockcheck__text">'
				delivery_availability_eis = '</span>'
				delivery_availability = ext_str(val=rep,sis=delivery_availability_sis,eis=delivery_availability_eis)
				np['delivery_availability'] = delivery_availability
				print('delivery_availability:',delivery_availability)
			except:
				err.append(val)

			try:
				op = read_pickle_file('products.pickle')
				op[val] = np
				write_pickle_file('products.pickle', op)
				t = read_pickle_file('products.pickle')
				print(t[val])
			except:
				err.append(val)


def get_view_count(pid):
	json_url = 'https://socialproof.api.useinsider.com/?partnerName=ikeauae&isUniqueView=false&campId=388&v=2&t=esCountAnalytics&dailyView=true&kkbRandomSettings[dailyStatus]=1&kkbRandomSettings[dailyStartVal]=11&kkbRandomSettings[dailyEndVal]=31&kkbRandomSettings[instantStatus]=0&kkbRandomSettings[instantStartVal]=0&kkbRandomSettings[instantEndVal]=0&kkbRandomSettings[dailyPurchaseStatus]=0&kkbRandomSettings[dailyPurchaseStartVal]=0&kkbRandomSettings[dailyPurchaseEndVal]=0&kkbRandomSettings[instantPurchaseStatus]=0&kkbRandomSettings[instantPurchaseStartVal]=0&kkbRandomSettings[instantPurchaseEndVal]=0&kkbRandomSettings[basketCountStatus]=0&kkbRandomSettings[basketCountStartVal]=0&kkbRandomSettings[basketCountEndVal]=0&ms[dms]=0&ms[dmv]=0&ms[dpms]=0&ms[dpmv]=0&ms[ims]=0&ms[imv]=0&ms[ipms]=0&ms[ipmv]=0&ms[bcms]=0&ms[bcmv]=0&addToOriginalSettings[dailyAddToOriginalStatus]=0&addToOriginalSettings[dailyAddToOriginalValue]=0&addToOriginalSettings[dailyPurchaseAddToOriginalStatus]=0&addToOriginalSettings[dailyPurchaseAddToOriginalValue]=0&addToOriginalSettings[instantAddToOriginalStatus]=0&addToOriginalSettings[instantAddToOriginalValue]=0&addToOriginalSettings[instantPurchaseAddToOriginalStatus]=0&addToOriginalSettings[instantPurchaseAddToOriginalValue]=0&addToOriginalSettings[basketCountAddToOriginalStatus]=0&addToOriginalSettings[basketCountAddToOriginalValue]=0&uniqueID='+pid
	f=requests.get(json_url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'})
	d=json.loads(f.text)
	return(d['count']['dailyView'])

def add_products_to_sql_db():
	for i,val in enumerate(products):
		print(products[val]['id'], f'Remaining: {len(products) - i}')
		try:
			new_product, created = Product.objects.get_or_create(
				pid = products[val]['id'],
				url = products[val]['url'],
				brand = products[val]['brand'],
				title = products[val]['title'],
				price = products[val]['price'],
				width = products[val]['width'],
				height = products[val]['height'],
				length = products[val]['length'],
				weight = products[val]['weight'],
				delivery_availability = products[val]['delivery_availability'],
				)
		except:
			err.append([products[val]['id']])

		if created:
			print(f'{products[val]["id"]} Added to DB.')

def add_upc_code():
	fn = 'History_1609245171733.csv'
	raw = read_csv_file(fn)
	sp = raw.split('\n')
	upc = []
	upc_cntr = 0
	in_db = {}
	tot = len(sp)
	err = []

	for idx,i in enumerate(sp):
		print(f'Remaining: {tot - idx}')
		if 'ITF' in i:
			full_upc = i.split(',')[4]
			upc.append(full_upc)
			pid = full_upc[:8]
			p=Product.objects.filter(pid=pid)
			if len(p) > 0:
				p.update(upc=full_upc)
				print(f'UPC Added \t{p[0].title} \t{p[0].url}')
				upc_cntr += 1
			else:
				err.append(full_upc)
	print('err=', len(err))
	write_file(str(err),'upc-err.txt')
	print(f'{upc_cntr} UPC\'s added')

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
	print(f'{len(sub_cats)} sub_cats extracted')
	return sub_cats

def check_for_new_products():
	sub_cats = get_sub_cats()
	nw_cntr = 0
	for idx,val in enumerate(sub_cats):
		print('val: ',val)
		cat_id = val.split('-')[-1].split('/')[0]
		json_url = f'https://sik.search.blue.cdtapps.com/ae/en/product-list-page?category={cat_id}&size=480'
		print('json_url:\t',json_url)
		try:
			f = urllib.request.urlopen(json_url)
			rep = str(f.read().decode("utf-8"))
			d=json.loads(rep)
			po=d['productListPage']['productWindow']
			print(f'Remainig: {len(sub_cats[227:])-idx}')
			for i in po:
				d={}
				pid = i['id']
				url = i['pipUrl']
				obj, created = Product.objects.update_or_create(
					pid=pid, url=url,
				)
				if created:
					nw_cntr += 1
					print('New product Added:  ',obj)
				else:
					print('Product Already exists: ',obj)
		except:
			pass



def update_product_details():
	check_for_new_products()
	err = []
	products = Product.objects.all()
	for i,val in enumerate(products):
		print(f'Remaining: {len(products)-i}',i)
		url = val.url
		print(url)
		try:
			f = urllib.request.urlopen(url)
			rep = str(f.read().decode("utf-8"))

			# try:
			# 	brand_sis = '<div class="range-revamp-header-section__title--big">'
			# 	brand_eis = '</div>'
			# 	brand = ext_str(val=rep,sis=brand_sis,eis=brand_eis)
			# 	val.update(brand=brand)
			# 	print('brand:',brand)
			# except:
			# 	err.append(val)
			brand_sis = '<div class="range-revamp-header-section__title--big">'
			brand_eis = '</div>'
			brand = ext_str(val=rep,sis=brand_sis,eis=brand_eis)
			Product.objects.filter(pk=val.pk).update(brand=brand)
			print('brand:',brand)
		except:
			pass


		try:
			title_sis = '<span class="range-revamp-header-section__description-text">'
			title_eis = '</span>'
			title = ext_str(val=rep,sis=title_sis,eis=title_eis)
			print('title:',title)
			Product.objects.filter(pk=val.pk).update(title=title)
		except:
			err.append(val)
		
		

		try:
			price_sis = '<span class="range-revamp-price__integer">'
			price_eis = '</span>'
			price = ext_str(val=rep,sis=price_sis,eis=price_eis)
			print('price:',price)
			Product.objects.filter(pk=val.pk).update(price=price)
		except:
			err.append(val)

		try:
			width_sis = 'class="range-revamp-product-details__label">Width: '
			width_eis = '</span><span class="range-revamp-product-details__label">Height:'
			width = ext_pkg(rep,width_sis,width_eis)
			print('width:',width)
			Product.objects.filter(pk=val.pk).update(width=width)
		except:
			err.append(val)

		try:
			height_sis = '</span><span class="range-revamp-product-details__label">Height: '
			height_eis = '</span><span class="range-revamp-product-details__label">Length: '
			height = ext_pkg(rep,height_sis,height_eis)
			print('height:',height)
			Product.objects.filter(pk=val.pk).update(height=height)
		except:
			err.append(val)

		try:
			length_sis = '</span><span class="range-revamp-product-details__label">Length: '
			length_eis = '</span><span class="range-revamp-product-details__label">Weight: '
			length = ext_pkg(rep,length_sis,length_eis)
			print('length:',length)
			Product.objects.filter(pk=val.pk).update(length=length)
		except:
			err.append(val)

		try:
			weight_sis = '</span><span class="range-revamp-product-details__label">Weight: '
			weight_eis = '</span><span class="range-revamp-product-details__label">Package(s):'
			weight = ext_pkg(rep,weight_sis,weight_eis)
			print('weight:',weight)
			Product.objects.filter(pk=val.pk).update(weight=weight)
		except:
			err.append(val)

		try:
			delivery_availability_sis = '<span class="range-revamp-stockcheck__text">'
			delivery_availability_eis = '</span>'
			delivery_availability = ext_str(val=rep,sis=delivery_availability_sis,eis=delivery_availability_eis)
			print('delivery_availability:',delivery_availability)
			Product.objects.filter(pk=val.pk).update(delivery_availability=delivery_availability)
		except:
			err.append(val)	


# check_for_new_products()
update_product_details()
# main_cats = read_pickle_file('main_cats.pickle')
# cats = read_pickle_file('cats.pickle')
# sub_cats = read_pickle_file('sub_cats.pickle')

