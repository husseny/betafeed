# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib, json, sys, requests, twitter

# Create your views here.

def index(request):
	host = request.META['HTTP_HOST'];
	if 'localhost' in host:
		host_name = 'http://'+host+'/'
	else:
		host_name = 'https://'+host+'/'
	#feed = get_reddit_feed(request)
	#twitter_feed = get_twitter_feed(request)
	feed= []
	twitter_feed = []
	return render(request, 'betahash/home.html', {'reddit_feed':json.dumps(feed), 'twitter_feed':json.dumps(twitter_feed)})

def get_twitter_feed(request):
	api = twitter.Api(consumer_key='3uHqK8RF4IevpfJAIgB7onZ1r', consumer_secret='2Ju8XPrlEhHCxZWoDTAIiswxl2YDjr9mlgwkArkYzcyRMdqgyi', access_token_key='172919027-5UtjjiNh5gjdBzAkcYmC3gN3mBa8TSeKTjmHuGlc',access_token_secret='NgzeVYmqpjlMAtYdO8MPcQq7ykX2PCZm51YMIzHcvyHEi')
	#print >>sys.stderr, api
	data1 = api.GetSearch(raw_query="q=%23betatesting&result_type=recent&since=2016-07-19&count=100")
	data2 = api.GetSearch(raw_query="q=%23betatesters&result_type=recent&since=2016-07-19&count=100")
	data3 = api.GetSearch(raw_query="q=%23Betatesting%20%23Betatesters&since=2016-07-19")
	data4 = api.GetSearch(raw_query="q=%23testmyapp&result_type=recent&since=2016-07-19")
	json_data = []
	data = data1 + data2 + data3 + data4
	for item in data:
		item = item._json
		print >>sys.stderr, item['user']['screen_name']
		json_data.append({'screen_name':item['user']['screen_name'], 'status_id': item['id'], 'tweet':item['text']})
	contains_filter = contains_key_value('screen_name', 'Instabug')
	not_contains_filter = not_contains_key_value('screen_name', 'Instabug')
	priority_result = filter(contains_filter, json_data)
	unprio_result = filter(not_contains_filter, json_data)
	result = priority_result + unprio_result
	print >>sys.stderr, len(data)
	return result

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
	contains_filter = contains_key_value('title', 'Instabug')
	not_contains_filter = not_contains_key_value('title', 'Instabug')
	priority_result = filter(contains_filter, result)
	unprio_result = filter(not_contains_filter, result)
	result = priority_result + unprio_result
	return result

def contains_key_value(key, uppercase_value):
	def containsFunc(element):
		return contains_word(element, key, uppercase_value)
	return containsFunc

def not_contains_key_value(key, uppercase_value):
	def containsFunc(element):
		return not contains_word(element, key, uppercase_value)
	return containsFunc

def contains_word(element, key, uppercase_value):
	return uppercase_value.lower() in element[key] or uppercase_value in element[key]