import urllib.request


def write_csv(val, file_name='replay.html'):
	try:
		with open(file_name, 'w') as the_file:
			the_file.write(val)
			print(file_name + ' exported')
	except:
		print("Couldn't export data :'(")

main_cats = ['https://www.ikea.com/ae/en/cat/furniture-fu001/', 'https://www.ikea.com/ae/en/cat/storage-organisation-st001/', 'https://www.ikea.com/ae/en/cat/beds-mattresses-bm001/', 'https://www.ikea.com/ae/en/cat/kitchen-appliances-ka001/', 'https://www.ikea.com/ae/en/cat/bathroom-products-ba001/', 'https://www.ikea.com/ae/en/cat/baby-children-bc001/', 'https://www.ikea.com/ae/en/cat/decoration-de001/', 'https://www.ikea.com/ae/en/cat/kitchenware-tableware-kt001/', 'https://www.ikea.com/ae/en/cat/textiles-tl001/', 'https://www.ikea.com/ae/en/cat/rugs-mats-flooring-rm001/', 'https://www.ikea.com/ae/en/cat/lighting-li001/', 'https://www.ikea.com/ae/en/cat/home-smart-hs001/', 'https://www.ikea.com/ae/en/cat/home-electronics-he001/', 'https://www.ikea.com/ae/en/cat/outdoor-products-od001/', 'https://www.ikea.com/ae/en/cat/pots-plants-pp001/', 'https://www.ikea.com/ae/en/cat/laundry-cleaning-lc001/', 'https://www.ikea.com/ae/en/cat/home-improvement-hi001/', 'https://www.ikea.com/ae/en/cat/safety-products-sp001/', 'https://www.ikea.com/ae/en/cat/leisure-travel-lt001/', 'https://www.ikea.com/ae/en/cat/summer-ss001/', 'https://www.ikea.com/ae/en/cat/winter-collections-wt001/']
cats = ['https://www.ikea.com/ae/en/cat/armchairs-chaise-longues-fu006', 'https://www.ikea.com/ae/en/cat/sofas-armchairs-fu003', 'https://www.ikea.com/ae/en/cat/wardrobes-19053', 'https://www.ikea.com/ae/en/cat/bookcases-shelving-units-st002', 'https://www.ikea.com/ae/en/cat/tv-media-furniture-10475', 'https://www.ikea.com/ae/en/cat/chests-of-drawers-drawer-units-st004', 'https://www.ikea.com/ae/en/cat/sideboards-buffets-console-tables-30454', 'https://www.ikea.com/ae/en/cat/cabinets-cupboards-st003', 'https://www.ikea.com/ae/en/cat/beds-bm003', 'https://www.ikea.com/ae/en/cat/tables-desks-fu004', 'https://www.ikea.com/ae/en/cat/bar-furniture-16244', 'https://www.ikea.com/ae/en/cat/cafe-furniture-19141', 'https://www.ikea.com/ae/en/cat/chairs-fu002', 'https://www.ikea.com/ae/en/cat/outdoor-furniture-od003', 'https://www.ikea.com/ae/en/cat/childrens-furniture-18767', 'https://www.ikea.com/ae/en/cat/trolleys-fu005', 'https://www.ikea.com/ae/en/cat/room-dividers-46080', 'https://www.ikea.com/ae/en/cat/nursery-furniture-45780']

f = urllib.request.urlopen("https://www.ikea.com/ae/en/cat/furniture-fu001/")
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
			# cats.append()
			print(r)
			cntr += 1
		except:
			pass

print(cntr)