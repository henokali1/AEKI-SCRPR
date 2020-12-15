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


main_cats = read_pickle_file('main_cats.pickle')
cats = read_pickle_file('cats.pickle')
sub_cats = read_pickle_file('sub_cats.pickle')
products = {}

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

extract_products()
