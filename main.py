import requests
import os
from dotenv import load_dotenv

def search_movie(url:str, api:str, movie_name:str):
    params = {
            'query': movie_name,
            'api_key': api
            }
    r = requests.get(url, params=params)
    print(r.json())

'''
def get_movie(url:str, api:str , movie_id:str):
    params = {
            'query': movie_name,
            'api_key': api
            }
    r = requests.get(url, params=params).json()
    full_data = r['results'][0]

    title = full_data['title']
    overview = full_data['overview']
    release_date = full_data['release_date']
    vote = full_data['vote_average']
    vote_formatted = str(vote)[0:3]
    
    return title, overview, release_date, vote_formatted
'''

load_dotenv()
API = os.getenv('API')

if not API:
    print('No API keys found.')
    exit()

URL = 'https://api.themoviedb.org/3/search/movie'

movie_name = input('Movie Name:')

search_movie(url=URL, movie_name=movie_name, api=API)














"""
title, overview, release_date, vote = search_movie(url=URL, api=API, movie_name=movie_name)

print(f'''
    =========================
           MOVIE SEARCH
    =========================
    Movie Name: {title}
    Release Date: {release_date}
    iMDB: {vote}
    Overview:
    {overview}''')
"""
