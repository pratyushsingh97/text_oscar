# Hit the IMDB API and Rotton Tomato API to retrieve movie ratings and summary
# Written by: Pratyush Singh 

import cast as ct
import reviews

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

def _fuzzy_match(movie_title:str) -> str:
    """Get the closest match to the requested movie title. Fuzzy matching 
    searches final_movies.csv file to return the closes match.
    
    Args:
    movie_title: the movie title requested by the user
    
    Returns:
    movie_title: a fuzzy matched movie_title
    """
    with open('resources/final_movies.csv', newline='') as movies_list:
        reader = csv.DictReader(movies_list)
        movies = [movie['Movie_Titles'].strip() for movie in reader]
        match, confidence = process.extract(movie_title, movies, limit=1, scorer=fuzz.token_sort_ratio)[0]
        
        if confidence >= 70:
            movie_title = match
        
    
    movies_list.close()
    
    return movie_title
            
            
def _preprocess_title(movie_title:str) -> str:
    ''' 
    This helper function takes the movie title and removes redundant spaces. 
    It also fuzzy matches the movie title, and it also formats movie titles 
    that are more than one word to be of the format "A+B+C". This format is 
    required to ping several APIs.
    
    Args:
    movie_title: raw movie title. 
    
    Returns:
    movie_title: cleaned movie title
    '''
    
    movie_title = movie_title.strip()
    movie_title = _fuzzy_match(movie_title)
    
    if ' ' in movie_title:
        movie_title_parts = movie_title.split()
        movie_title_parts = [parts.strip() for parts in movie_title_parts]
        operator = "+"
        movie_title = operator.join(movie_title_parts)
    
    return movie_title

def _check_for_ratings_keys(rating_json:json, reviewer_key:str) -> int:
    """Parses the OMDB response for the imdb and rotten tomatoes 
    ratings for a movie.
    
    Returns the index at which the rating resides in the json response 
    
    Args:
    ratings_json: json response containing moving metadata from OMDB
    reviewer_key: either 'Rotten Tomatoes' or 'IMDB'. 
    """
    
    exists = False
    
    for idx, reviewer in enumerate(rating_json):
        if reviewer_key in reviewer['Source']:
            return idx
    
    return None
    

def _format_response(json_response:json) -> dict:
    """ A helper method that formats the text message response to the user.
    
    Args:
    json_response: the movie metadata information from OMDB 
    
    Returns:
    response: a dictionary that contains a essential movie information along 
    with the summary of the movie.
    """
    
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
        
    
    movie_info = response_template.substitute(movie_title=movie_title,
                                rating=rating,
                                director=directors,
                                cast=cast_members,
                                plot=plot,
                                imdb=imdb,
                                rt=rt)
    
    
    review = reviews.reviews(movie_title)
    
    response = {"movie_information": movie_info, "review_nyt": str(review)}
    
    return response
        

# @TODO: Return an appropriate error message
def _movie_information(movie_title:str=None) -> json:
    """ Retrieves movie metadata by pinging the OMDB (Open Movie Database)
    
    Args: 
    movie_title: the movie requested
    movie_data: json response containing the movie metadata 
    """
    try:
        movie_title = _preprocess_title(movie_title)
        
        api = config['API']
        imdb_key = api['IMDB']
        imdb_api = f"http://www.omdbapi.com/?t={movie_title}&y=2019&plot=full&apikey={imdb_key}"
        
        movie_data = requests.get(imdb_api).text
        movie_data = json.loads(movie_data)
        
        if movie_data is None:
            return "Error has Occurred!"
        
        if 'Response' in movie_data.keys():
            if movie_data['Response'] == 'False':
                return f"Unable to retrieve {movie_title}"
    
    except Exception as e:
        print(e)
        return "Error has Occurred!"
    
    return movie_data


def get_movie_metadata(title:str) -> json:
    """ Runner function that retrieves the data about the movie
    
    Args:
    title: movie title 
    
    Returns:
    movie_md: json of movie metadata
    """
    
    if title is None:
        return "Error!" 
    
    if not len(title.strip()):
        return "Pass a movie title"
    
    movie_data = _movie_information(movie_title=title)
    movie_md = _format_response(movie_data) if movie_data != f"Unable to retrieve {title}" else movie_data
    
    return movie_md

        