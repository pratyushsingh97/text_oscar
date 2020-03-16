# Scrape movie reviews from ny times 
# Written by: Pratyush Singh
''' This file pings the NYT API and retrieves the link to the reviews. 
If a review is present, then the 'review_text' column is filled with "test". If
no review is present, then the column is filled with "NA".
'''
import csv
import requests
import json
import time

from configparser import ConfigParser
from datetime import datetime as dt

import pandas as pd

from tqdm import tqdm

YEAR = 2019

def movie_list() -> list:
    """Retrieve the movies from the final_movies.csv. This file contains
    all the movies that were released in 2019. 
    """
    movies = []
    with open('../phase1/resources/final_movies.csv', newline='') as movies_list:
        reader = csv.DictReader(movies_list)
        movies = [movie['Movie_Titles'].strip() for movie in reader]
    
    movies_list.close()
    

    return movies


def review_link(movie_title):
    '''
    Return -1 if no review or the movie is not in 2019
    Return the url of the movie 
    '''
    config = ConfigParser()
    config.read('../phase1/conf.ini')
    
    nyt_key = config['API']['NYT_API_KEY']
    api_req = f"https://api.nytimes.com/svc/movies/v2/reviews/search.json?order=by-year&query={movie_title}&api-key={nyt_key}"
    response = requests.get(api_req).text
    response = json.loads(response)
    
    try:
        if response['status'] == "OK":
            if response['num_results'] >= 1:
                results = response['results'][0]
                release_str = results['opening_date']
                date = dt.strptime(release_str, "%Y-%m-%d")
                
                if date.year >= YEAR:
                    if results['link']['type'] == 'article':
                        return results['link']['url']

    except Exception as e:
        print(movie_title)
        print(e)
                    
    return -1


def scrape(url):
    return "testing"
        
     

def runner():
    """Constructs the pandas DataFrame with the movie information"""
    review_df = {"movie_title": [], "article_link": [], "text": []}
    
    movies = movie_list()
    
    for idx, movie in enumerate(tqdm(movies)):
        # extra cleaning 
        movie = movie.replace('\'', "")
        movie = movie.replace('\"', "")
        movie = movie.strip()
        
        results = review_link(movie)
        review_df['article_link'].append(results)
        review_df['movie_title'].append(movie)
        
        if results != -1:
            scraped_text = scrape(results)
            review_df['text'].append(scraped_text)
        else:
            review_df['text'].append("NA")
        
        time.sleep(8)
        
        if idx % 10 == 0:
            temp_df = pd.DataFrame(review_df)
            temp_df.to_csv('nytimes.csv')
    
    review_df = pd.DataFrame(review_df)
    review_df.to_csv("test.csv")


runner()
        
        
        
    