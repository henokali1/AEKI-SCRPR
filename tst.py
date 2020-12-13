import urllib.request
from time import sleep
import pickle
import io

def read_pickle_file(fn):
	try:
		with open(fn, 'rb') as handle:
			f = pickle.load(handle)
		return f
	except:
		print(f"Couldn't read {fn}")

def write_pickle_file(fn):
	try:
		with open(fn, 'wb') as handle:
			pickle.dump(fn, handle, protocol=pickle.HIGHEST_PROTOCOL)
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

def get_no_of_pages(url):
	f = urllib.request.urlopen(url)
	rep = str(f.read().decode("utf-8"))
	print(rep)
	write_file(rep)
	print(type(rep))

def extract_products():
	for idx,val in enumerate(sub_cats[0:1]):
		print(val)
		# get_no_of_pages(val)

# extract_products()
url = 'https://www.ikea.com/ae/en/cat/paper-media-boxes-16202/'
f = urllib.request.urlopen(url)
rep = str(f.read().decode("utf-8"))
write_file(rep)
