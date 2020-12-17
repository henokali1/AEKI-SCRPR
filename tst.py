import urllib.request
from time import sleep
import pickle
import ast
import io
import json

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

main_cats = read_pickle_file('main_cats.pickle')
cats = read_pickle_file('cats.pickle')
sub_cats = read_pickle_file('sub_cats.pickle')
products = read_pickle_file('products.pickle')

def extract_products():
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


err=[]
extract_product_details()
print(err)
