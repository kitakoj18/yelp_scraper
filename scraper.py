import numpy as np 
import pandas as pd 

import requests
from bs4 import BeautifulSoup

import time
import pickle

def scrape_pages(url, num_pages=1, sleep=60):

	reviews = []
	review_dates = []
	review_ratings = [] 

	for i in range(1, num_pages+1):

		page_start = (i-1)*20
		page_url = url + '?start={}'.format(page_start) 
		page = requests.get(page_url)
		soup = BeautifulSoup(page.text, 'lxml')

		#get reviews and map each to text
		reviews_tags = soup.findAll('p', {'itemprop': 'description'})
		reviews_texts = map(lambda x:x.text, reviews_tags)
		reviews.extend(reviews_texts)
		print(len(reviews))

		#get posted date of each review
		review_date_tags = soup.findAll('meta', {'itemprop': 'datePublished'})
		review_date_content = map(lambda x:x['content'], review_date_tags)
		review_dates.extend(review_date_content)
		print(len(review_dates))

		#get rating of each review
		review_rating_tags = soup.findAll('div', {'itemprop': 'reviewRating'})
		review_rating_content = map(lambda x:x.find('meta', {'itemprop': 'ratingValue'})['content'], review_rating_tags)
		review_ratings.extend(review_rating_content)
		print(len(review_ratings))

		if i != num_pages:
			time.sleep(sleep)

	data_dict = {'reviews': reviews, 'review_dates': review_dates, 'review_ratings': review_ratings}

	df = pd.DataFrame.from_dict(data_dict)

	return df

if __name__ == '__main__':

	url = 'https://www.yelp.com/biz/nothing-but-coffee-los-angeles'
	df_nbc = scrape_pages(url, 9)

	# with open('df_nbc.pickle', 'wb') as handle:
	# 	pickle.dump(df_nbc, handle, protocol=pickle.HIGHEST_PROTOCOL)

	# with open('df_nbc.pickle', 'rb') as handle:
	# 	df_nbc = pickle.load(handle)

