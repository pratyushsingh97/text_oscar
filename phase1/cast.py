# Written By: Pratyush Singh
import json
import requests
from configparser import ConfigParser

config = ConfigParser()
config.read('conf.ini')

# @TODO: Add error catching
def _tmdb_id(imdb_id:int) -> int:
    """Uses the imdb id of the movie to query the OMDB database id.
    The OMDB id is used to retrieve the cast of the movie from the OMDB API
    
    Args:
    imdb_id: a unique key for the movie requested 
    
    Returns:
    tomdb: a unique key for the same movie in the movie database.
    """
    try:
        tmdb_key = config['API']['TMDB']
        tmdb_api = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={tmdb_key}&language=en-US&external_source=imdb_id"
        results = requests.get(tmdb_api).text
        results = json.loads(results)
    
        return results['movie_results'][0]['id']
    
    except Exception as e:
        print(e)
        
        return -1
    
def cast(imdb_id):
    # only get the top 5 cast members
    tmdb_id = _tmdb_id(imdb_id)
    
    if tmdb_id != -1:
        try:
            cast_list = []
            
            # retrive the cast 
            tmdb_key = config['API']['TMDB']
            tmdb_cast_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits?api_key={tmdb_key}"
            results = requests.get(tmdb_cast_url).text
            results = json.loads(results)
            cast_members = results['cast'][0:6]
            
            cast_list = [cast_member['name'] for cast_member in cast_members]
            
            sep = ", "
            cast_list = sep.join(cast_list)
            
            return cast_list

        except Exception as e:
            print(e)
            
            return -1
        
        
        
    
    

