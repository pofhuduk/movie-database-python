import requests
import os
from dotenv import load_dotenv

def search_movie(url:str, api:str, movie_name:str):
    params = {
            'query': movie_name,
            'api_key': api
            }
    r = requests.get(url, params=params).json()
    results = r['results']
    
    if (len(results) == 1):
        return False
    text= ''
    for index, obj in enumerate(results[0:7]):
        text += f'[{index + 1}] '+ obj['title'] + ' | ' + obj['release_date'] + '\n'
     
    return text

def get_movie(url:str, api:str , movie_name:str, index:int):
    params = {
            'query': movie_name,
            'api_key': api
            }
    r = requests.get(url, params=params).json()
    full_data = r['results']
    movie = full_data[index]

    title = movie['title']
    overview = movie['overview']
    release_date = movie['release_date']
    vote = movie['vote_average']
    vote_formatted = str(vote)[0:3]
    
    return title, release_date, vote_formatted, overview
    
load_dotenv()
API = os.getenv('API')

if not API:
    print('No API keys found.')
    exit()

URL = 'https://api.themoviedb.org/3/search/movie'

def main(api:str, url:str):
    movie_name = input('Movie Name:')
    
    results = search_movie(url=url, movie_name=movie_name, api=api)
    if not results:
        index = 0
    else:
        choice = input(results)
        index = int(choice) - 1

    title, release_date, vote, overview = get_movie(
            url=url,
            movie_name=movie_name,
            api=api,
            index=index)

    print(f'''
        =========================
               MOVIE SEARCH
        =========================
        Movie Name: {title}
        Release Date: {release_date}
        iMDB: {vote}
        Overview:
        {overview}''')


while True:
    main(api=API, url=URL)
