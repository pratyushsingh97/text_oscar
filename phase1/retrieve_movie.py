# Hit the IMDB API and Rotton Tomato API to retrieve movie ratings and summary 

import cast as ct

import requests 
import json
import asyncio
import csv

from configparser import ConfigParser
from string import Template
from pprint import pprint

from fuzzywuzzy import fuzz, process

config = ConfigParser()
config.read('conf.ini')

def _fuzzy_match(movie_title):
    with open('resources/final_movies.csv', newline='') as movies_list:
        reader = csv.DictReader(movies_list)
        movies = [movie['Movie_Titles'].strip() for movie in reader]
        match, confidence = process.extract(movie_title, movies, limit=1, scorer=fuzz.token_sort_ratio)[0]
        
        print(match, confidence)
        
        if confidence >= 70:
            movie_title = match
        
    
    movies_list.close()
    
    return movie_title
            
            
def _preprocess_title(movie_title):
    ''' 
    This helper function takes the movie title and removes redundant spaces.
    It also formats movie titles that are more than one word to be of the format
    "A+B+C"
    '''
    
    movie_title = movie_title.strip()
    movie_title = _fuzzy_match(movie_title)
    
    if ' ' in movie_title:
        movie_title_parts = movie_title.split()
        movie_title_parts = [parts.strip() for parts in movie_title_parts]
        operator = "+"
        movie_title = operator.join(movie_title_parts)
    
    return movie_title

def _check_for_ratings_keys(rating_json, reviewer_key):
    exists = False
    
    for idx, reviewer in enumerate(rating_json):
        if reviewer_key in reviewer['Source']:
            return idx
    
    return None
    

def _format_response(json_response):
    response_template = Template("$movie_title ($rating)\n" + 
                                 "Directed By: $director\n" + 
                                 "Cast: $cast\n\n" + 
                                 "$plot\n\n" + 
                                 "IMDB: $imdb\n" + 
                                 "Rotton Tomatoes: $rt")
    
    movie_title, rating, directors, cast_members, plot, imdb, rt = ("", "", "", "",
                                                            "", "", "")
    
    keys = json_response.keys()
    
    if 'Title' in keys:
        movie_title = json_response['Title']
    if 'Rated' in keys:
        rating = json_response['Rated']
    if 'Director' in keys:
        directors = json_response['Director']
    if 'Plot' in keys:
        plot = json_response['Plot']
    if 'Ratings' in keys:
        imdb_index = _check_for_ratings_keys(json_response['Ratings'], 'Internet Movie Database')
        rt_index = _check_for_ratings_keys(json_response['Ratings'], 'Rotten Tomatoes') 
        
        imdb = json_response['Ratings'][imdb_index]['Value'] if imdb_index != None else ""
        rt = json_response['Ratings'][rt_index]['Value'] if rt_index != None else ""
    
    
    # get the cast 
    if 'imdbID' in keys:
        imdb_id = json_response['imdbID']
        cast_members = ct.cast(imdb_id)
        
    
    response = response_template.substitute(movie_title=movie_title,
                                rating=rating,
                                director=directors,
                                cast=cast_members,
                                plot=plot,
                                imdb=imdb,
                                rt=rt)
    
    return response
        

# @TODO: Return an appropriate error message
def retrieve_movie_metadata(movie_title=None):
    if movie_title is None:
        return "Error!" 
    
    try:
        movie_title = _preprocess_title(movie_title)
        
        api = config['API']
        imdb_key = api['IMDB']
        imdb_api = f"http://www.omdbapi.com/?t={movie_title}&y=2019&plot=full&apikey={imdb_key}"
        
        movie_data = requests.get(imdb_api).text
        movie_data = json.loads(movie_data)
        
        if movie_data is None:
            return "Error has Occurred!"
    
    except Exception as e:
        print(e)
        return "Error has Occurred!"
    
    return movie_data


def get_movie_metadata(title):
    movie_data = retrieve_movie_metadata(movie_title=title)
    movie_md = _format_response(movie_data)
    
    return movie_md
        