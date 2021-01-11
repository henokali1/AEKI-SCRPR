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
import time
import datetime

def ext_str(val, sis, eis):
	try:
		si = val.index(sis)+len(sis)
		ei = val[si:].index(eis)+si
		return val[si:ei]
	except:
		pass
		# print('Err', val)

def get_view_count(pid):
	json_url = 'https://socialproof.api.useinsider.com/?partnerName=ikeauae&isUniqueView=false&campId=388&v=2&t=esCountAnalytics&dailyView=true&kkbRandomSettings[dailyStatus]=1&kkbRandomSettings[dailyStartVal]=11&kkbRandomSettings[dailyEndVal]=31&kkbRandomSettings[instantStatus]=0&kkbRandomSettings[instantStartVal]=0&kkbRandomSettings[instantEndVal]=0&kkbRandomSettings[dailyPurchaseStatus]=0&kkbRandomSettings[dailyPurchaseStartVal]=0&kkbRandomSettings[dailyPurchaseEndVal]=0&kkbRandomSettings[instantPurchaseStatus]=0&kkbRandomSettings[instantPurchaseStartVal]=0&kkbRandomSettings[instantPurchaseEndVal]=0&kkbRandomSettings[basketCountStatus]=0&kkbRandomSettings[basketCountStartVal]=0&kkbRandomSettings[basketCountEndVal]=0&ms[dms]=0&ms[dmv]=0&ms[dpms]=0&ms[dpmv]=0&ms[ims]=0&ms[imv]=0&ms[ipms]=0&ms[ipmv]=0&ms[bcms]=0&ms[bcmv]=0&addToOriginalSettings[dailyAddToOriginalStatus]=0&addToOriginalSettings[dailyAddToOriginalValue]=0&addToOriginalSettings[dailyPurchaseAddToOriginalStatus]=0&addToOriginalSettings[dailyPurchaseAddToOriginalValue]=0&addToOriginalSettings[instantAddToOriginalStatus]=0&addToOriginalSettings[instantAddToOriginalValue]=0&addToOriginalSettings[instantPurchaseAddToOriginalStatus]=0&addToOriginalSettings[instantPurchaseAddToOriginalValue]=0&addToOriginalSettings[basketCountAddToOriginalStatus]=0&addToOriginalSettings[basketCountAddToOriginalValue]=0&uniqueID='+pid
	f=requests.get(json_url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'})
	d=json.loads(f.text)
	return(d['count']['dailyView'])

def update_view_cnt():
	err = []
	cntr = 0
	products = Product.objects.all()
	for i in products:
		# print(i.pid, f'Remaining: {6330 - cntr}')
		cntr += 1
		try:
			new_daily_view, created = dailyViewCount.objects.get_or_create(
				count = get_view_count(i.pid),
				product = i,
				)
		except:
			err.append([i.pid])
		# new_daily_view, created = dailyViewCount.objects.get_or_create(
		# 	count = get_view_count(i),
		# 	product = i.pk,
		# 	)


		# if created:
		# 	print(f'{i.pid} Added to DB.')
		# else:
		# 	print(f'{i.pid} Already Exists.')
		
		avg_cnt = dailyViewCount.objects.filter(product=i.pk).aggregate(Avg('count'))
		avg_cnt = int(avg_cnt['count__avg'])
		Product.objects.filter(pk=i.pk).update(avg_view=avg_cnt)

def calc_tm():
	et = time.time()
	tt = int((et-st)/60)
	hrs = int(tt/60)
	mins = tt%60
	print(f'Task completed in: {hrs}:{mins}')

st = time.time()
print(f'------------ Start {datetime.datetime.now()} ------------')
update_view_cnt()
calc_tm()
print(f'------------ End {datetime.datetime.now()} ------------\n\n')
