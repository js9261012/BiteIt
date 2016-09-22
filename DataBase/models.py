from django.db import models

class StoreInfo(models.Model):
	google_store_id = models.CharField(max_length=200, unique=True)  
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	url = models.CharField(max_length=500, null=True)
	email = models.EmailField(max_length=254, null=True)
	longitude = models.DecimalField(max_digits=35, decimal_places=28)
	latitude = models.DecimalField(max_digits=35, decimal_places=28)
	first_level = models.CharField(max_length=200)
	third_level = models.CharField(max_length=200)
	tags = models.CharField(max_length=500)

class NotQueryLocation(models.Model):
	#mapping_id = models.CharField(max_length=200, unique=True)
	notQuerylongitude = models.DecimalField(max_digits=35, decimal_places=28)
	notQuerylatitude = models.DecimalField(max_digits=35, decimal_places=28)
	notQueryradius = models.DecimalField(max_digits=35, decimal_places=28)
	query_level = models.CharField(max_length=200)
	isQuery = models.BooleanField(default=False)

class MappingLocation(models.Model):
	c_lat = models.DecimalField(max_digits=35, decimal_places=28, unique=True)
	c_lng = models.DecimalField(max_digits=35, decimal_places=28, unique=True)
	bound_right_lng = models.DecimalField(max_digits=35, decimal_places=28)
	boubd_left_lng = models.DecimalField(max_digits=35, decimal_places=28)
	bound_up_lat = models.DecimalField(max_digits=35, decimal_places=28)
	bound_down_lat = models.DecimalField(max_digits=35, decimal_places=28)
	radius = models.DecimalField(max_digits=35, decimal_places=28)
	isFinish = models.BooleanField(default=False)