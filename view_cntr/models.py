from django.utils import timezone
from datetime import datetime
from django.db import models


class Product(models.Model):
	pid = models.CharField(max_length=250, default="")
	url = models.CharField(max_length=250, default="")
	brand = models.CharField(max_length=250, default="")
	title = models.CharField(max_length=250, default="")
	price = models.FloatField(default=0.0)
	width = models.FloatField(default=0.0)
	height = models.FloatField(default=0.0)
	length = models.FloatField(default=0.0)
	weight = models.FloatField(default=0.0)
	delivery_availability = models.CharField(max_length=250, default="")
	avg_view = models.IntegerField(default=0)
	is_fav = models.BooleanField(default=False)
	is_listed = models.BooleanField(default=False)
	upc = models.CharField(max_length=250, default="")

	def __str__(self):
		return str(self.pk) + ' - ' + self.pid + ' - ' + self.title

class dailyViewCount(models.Model):
	date = models.DateField(default=datetime.now)
	count = models.IntegerField(default=0)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.date) + ' - ' + str(self.count)
