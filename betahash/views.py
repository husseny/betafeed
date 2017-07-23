# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib, json, sys, requests

# Create your views here.

def index(request):
	host = request.META['HTTP_HOST'];
	if 'localhost' in host:
		host_name = 'http://'+host+'/'
	else:
		host_name = 'https://'+host+'/'
	feed = get_reddit_feed(request)
	return render(request, 'betahash/home.html', {'reddit_feed':json.dumps(feed)})

def get_twitter_feed(request):

def get_reddit_feed(request):
	url = "http://www.reddit.com/r/AndroidAppTesters/new.json?sort=new"
	response = requests.get(url, headers = {'User-agent': 'betahash 0.1'})
	data1 = response.json()
	data1 = data1['data']
	url = "https://www.reddit.com/r/alphaandbetausers/new.json?sort=new"
	response = requests.get(url, headers = {'User-agent': 'betahash 0.1'})
	data2 = response.json()
	data2 = data2['data']
	url = "https://www.reddit.com/r/TestMyApp/new.json?sort=new"
	response = requests.get(url, headers = {'User-agent': 'betahash 0.1'})
	data3 = response.json()
	data3 = data3['data']
	result = []
	data_array = data1['children'] + data2['children'] + data3['children']
	for item in data_array:
		item_data = item['data']
		result.append({'url': item_data['url'], 'title': item_data['title']})
	priority_result = filter(containsInstabug, result)
	unprio_result = filter(notcontainsInstabug, result)
	result = priority_result + unprio_result
	#print >>sys.stderr, len(result2)
	return result


def containsInstabug(element):
	return 'instabug' in element['title'] or 'Instabug' in element['title']

def notcontainsInstabug(element):
	return not containsInstabug(element)