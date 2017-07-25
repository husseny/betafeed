# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib, json, sys, requests, twitter, time
from datetime import datetime

# Create your views here.

def index(request):
	host = request.META['HTTP_HOST'];
	if 'localhost' in host:
		host_name = 'http://'+host+'/'
	else:
		host_name = 'https://'+host+'/'
	feed = get_reddit_feed(request)
	twitter_feed = get_twitter_feed(request)
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
		datetime_object = datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
		date = pretty_date(datetime_object)
		json_data.append({'screen_name':item['user']['screen_name'], 'user_name':item['user']['name'], 
			'date':date, 'profile_image': item['user']['profile_image_url_https'], 
			'status_id': item['id_str'], 'tweet':item['text']})
	contains_filter = contains_key_value('screen_name', 'Instabug')
	not_contains_filter = not_contains_key_value('screen_name', 'Instabug')
	priority_result = filter(contains_filter, json_data)
	unprio_result = filter(not_contains_filter, json_data)
	result = priority_result + unprio_result
	#print >>sys.stderr, len(data)
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
		created_at = datetime.fromtimestamp(item_data['created'])
		date = pretty_date(created_at)
		result.append({'url': item_data['url'], 'comments': item_data['permalink'], 
			'user_name': item_data['author'], 'title': item_data['title'], 'date': date})
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

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    diff = ""
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"