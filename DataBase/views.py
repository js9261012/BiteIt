from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import redirect
from DataBase.models import StoreInfo
from DataBase.models import MappingLocation
from DataBase.models import NotQueryLocation
from django.core import serializers
from collections import defaultdict

import algorithm
import json
import urllib
import urllib2
import locale
import requests
import decimal

x = 0
y = 0

key = '&key=AIzaSyBOocdmpIK7ljeKaY1IifN_oBorQn1CKwg&language=zh-TW'
reference_search = 'https://maps.googleapis.com/maps/api/place/details/json?reference='
nextToken_search = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken='


def reference_request(reference_url):
	url_end = reference_url + '&sensor=true' + key
	url = reference_search + url_end

	response = urllib.urlopen(url)
	data = json.loads(response.read())
	p =''
	try:
		p = data['result']['formatted_phone_number']
	except:
		p = ''

	first_long_name = ""
	third_long_name = ""

	for addressData in data['result']['address_components']:
		for leveData in addressData['types']:
			if leveData == 'administrative_area_level_1':
				first_long_name = addressData['long_name']
			if leveData == 'administrative_area_level_3':
				third_long_name = addressData['long_name']

	referenceData = [p, first_long_name, third_long_name]


	return referenceData

def isNextPage_two(nextPage_two):
	url_end = nextPage_two + '&sensor=true' + key
	url = nextToken_search + url_end

	response = urllib.urlopen(url)
	data = json.loads(response.read())
	locationList = []
	for result in data['results']:
		referenceData = reference_request(result['reference'])
		phone = referenceData[0]
		first_level = referenceData[1] 
		third_level = referenceData[2] 
		p = StoreInfo(google_store_id = result['id'], name = result['name'], address = result['vicinity'], url = None, email = None, latitude = result['geometry']['location']['lat'], longitude = result['geometry']['location']['lng'], phone = phone, first_level = first_level, third_level = third_level, tags = "")

		try:
			p.save()
		except:
			pass	
		locationList.append(result['geometry']['location']['lng'])

		
	return HttpResponse(locationList) 


def isNextPage_one(nextPage_one):
	url_end = nextPage_one + '&sensor=true' + key
	url = nextToken_search + url_end

	response = urllib.urlopen(url)
	data = json.loads(response.read())
	locationList = []
	for result in data['results']:
		referenceData = reference_request(result['reference'])
		phone = referenceData[0]
		first_level = referenceData[1]
		third_level = referenceData[2]
		p = StoreInfo(google_store_id = result['id'], name = result['name'], address = result['vicinity'], url = None, email = None, latitude = result['geometry']['location']['lat'], longitude = result['geometry']['location']['lng'], phone = phone, first_level = first_level, third_level = third_level, tags = "")

		try:
			p.save()
		except:
			pass	
		locationList.append(result['geometry']['location']['lng'])
	try:
		if data['next_page_token'] != None:
			isNextPage_two(data['next_page_token'])
	except:
		pass	
	return HttpResponse(locationList)
	 

def results(latitude, longitude, radius, level):
		lat = str(latitude)
		lng = str(longitude)
		rds = str(radius)
		
		 

		url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + lat + ',' + lng + '&radius='+ rds +'&types=food&sensor=false' + key
		
		response = urllib.urlopen(url)
		data = json.loads(response.read())

		#try:
		if data['status'] == 'OVER_QUERY_LIMIT':
			notQuery = NotQueryLocation(notQuerylatitude = latitude, notQuerylongitude = longitude, notQueryradius = radius, query_level = level, isQuery = False)
			notQuery.save()
		#except:
			#pass

		locationList = []
		for result in data['results']:
			referenceData = reference_request(result['reference'])
			phone = referenceData[0]
			first_level = referenceData[1]
			third_level = referenceData[2]
			p = StoreInfo(google_store_id = result['id'], name = result['name'], address = result['vicinity'], url = None, email = None, latitude = result['geometry']['location']['lat'], longitude = result['geometry']['location']['lng'], phone = phone, first_level = first_level, third_level = third_level, tags = "")
			
			try:
				p.save()
			except:
				pass	
			locationList.append(result['geometry']['location']['lng'])

		try:
			if data['next_page_token'] != None:
				isNextPage_one(data['next_page_token'])
		except:
			pass

		print(x)


		
def requestMap(request):
	c_lat = '25.034279'
	c_lng = '121.508004'
	b_right_lng = '121.510751'
	b_left_lng = '121.507543'
	b_up_lat = '25.036398'
	b_down_lat = '25.033706'
	r = '60'
	url = 'http://163.21.245.128:8000/mapping/route/?c_lng=' + c_lng + '&c_lat=' + c_lat + '&b_left_lng=' + b_left_lng + '&b_right_lng=' + b_right_lng + '&b_up_lat=' + b_up_lat + '&b_down_lat=' + b_down_lat +'&r=' + r


	response = urllib2.urlopen(url)
	data = json.loads(response.read())
	radius = data['r']
	
	
	for result_first in data['first']:
		results(result_first['latitude'], result_first['longitude'],radius, 'first')
			
	for result_second in data['second']:
		results(result_second['latitude'], result_second['longitude'], radius, 'second')

	try:
		p = MappingLocation(c_lat=c_lat, c_lng=c_lng, bound_right_lng=b_right_lng, boubd_left_lng=b_left_lng, bound_up_lat=b_up_lat, bound_down_lat=b_down_lat, radius=r, isFinish=False)
		p.save()
	except:
		pass

	return HttpResponse(y)


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)

def listall(request):
	raw_data = serializers.serialize("python", StoreInfo.objects.all())
	
	url = 'http://163.21.245.128:8888/api-biteit/api/authprofession/'
	url2 = 'http://163.21.245.128:8888/api-biteit/auth-storeinfo/'
	headers = {'Authorization': 'Basic Yml0ZWl0OmNqLzZiam80NWovIA==', 'Content-Type':'application/json '}
	r = requests.post(url, headers = headers)

	z = []
	for d in raw_data:
		if (d['fields']['email'] is None) or (d['fields']['email'] is ''):
			d['fields']['email'] = 'aero@gmail.com'
		d['fields']['ratingClean'] = 0
		d['fields']['ratingUnknow'] = 0
		d['fields']['ratingAtmos'] = 0
		d['fields']['ratingService'] = 0
		d['fields']['ratingFlavor'] = 0
		d['fields']['tags'] = " "
		d['fields']['url'] = 'null'
		data = json.dumps(d['fields'], default=decimal_default)
		res = requests.post(url2, data = data, headers = headers)
		z.append(res)
	
	# z = requests.post(url2, data = data, headers = headers)
	return HttpResponse(z)

def showStoreInfo(requests):
	show_data = serializers.serialize("json", StoreInfo.objects.all())
	return HttpResponse(show_data)

def showMappingLocation(requests):
	show_data = serializers.serialize("json", MappingLocation.objects.all())
	return HttpResponse(show_data)

def showNotQueryLocation(requests):
	show_data = serializers.serialize("json", NotQueryLocation.objects.all())
	return HttpResponse(show_data)


