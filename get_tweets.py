#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import json
import re
#Twitter API credentials
consumer_key = "qiOaRLVPldazXmYmF3IaIQw4L"
consumer_secret = "FAzcCMF1UUyuNuSeddAA1nDJYPeXm6OhaCD084k1t3BZ0HleCY"
access_key = "717220472623071233-oeDgXLyYdqT92Mi06aaAGV7EtSExfKS"
access_secret = "tVh6WAqVqJ5Pekb3skPON4OD46dyyBAIGOiWjPkZrtglC"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200,tweet_mode='extended')
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest,tweet_mode='extended')
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))



	for tweet in alltweets:
		if 'retweeted_status' in tweet._json.keys():
			alltweets.remove(tweet)
	p_list = []
	v_list = []
	url = []
	hashes = []
	for tweet in alltweets:
			v_count = 0
			p_count = 0
			if 'media' in tweet.entities:
				for image in  tweet.entities['media']:
					# print image['media_url']
					p_count += 1
			# if 'SAMVADA' in tweet._json['text']:
				# print (tweet._json)['entities']['media']
			if hasattr(tweet, 'extended_entities'):
				# print tweet.extended_entities
				if tweet.extended_entities['media'][0]['type'] =='photo':
					# print tweet.extended_entities['media'][0]
					p_count = p_count +1
				else: 
					v_count = v_count+1

			if 'urls' in (tweet._json)['entities'].keys():
				if ((tweet._json)['entities']['urls']):
					# print (tweet._json)['entities']['urls']
					if 'youtu.be' in str((tweet._json)['entities']['urls']):
						v_count = v_count + 1
			if (p_count==v_count) and (v_count==1):
				p_count = 0
				v_count = 1
			p_list.append(p_count)
			v_list.append(v_count)
			if re.search(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})',tweet.full_text):
				# print re.findall(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})',tweet.text)
				url.append(1)
			else:
				url.append(0)
			if 'hashtags' in tweet.entities.keys():
				hashes.append((tweet.entities['hashtags']))
			else:
				hashes.append(' ')
	#Not considering retweeted tweeets.	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8"), tweet.retweet_count, tweet.favorite_count] for tweet in alltweets]
	
	for i in range(len(outtweets)):
		outtweets[i].append(p_list[i])
		outtweets[i].append(v_list[i])
		outtweets[i].append(url[i])
		outtweets[i].append(hashes[i])
	# print outtweets
	# #write the csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text", "retweet_count","favorite_count","photos","videos","url",'hashes'])
		writer.writerows(outtweets)
	
	# pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("BJP4India")
	# get_all_tweets("iiit_hyderabad")