import requests
import os
from dotenv import load_dotenv
import subprocess
from typing import Literal

def search(url:str, api:str, name:str):
    params = {
            'query': name,
            'api_key': api
            }
    r = requests.get(url, params=params).json()
    results = r['results'] 
    return results

def get_info(media_list:list, index:int, media_type: Literal['movie' , 'tv']):
    media = media_list[index]
    
    match media_type:
        case 'movie':
            title = media['title']
            release_date = media['release_date']
        case 'tv':
            title = media['name']
            release_date = media['first_air_date']
        case _:
            raise ValueError(f'Wrong media_type: "{media_type}" ! '
            'You can only choose "movie" or "tv".') 
         
    overview = media['overview']
    vote_average = media['vote_average']
    vote_formatted = f"{vote_average:.1f}"
    
    return {
            'title': title,
            'overview': overview,
            'release_date': release_date,
            'average_vote': vote_formatted
            }

def list_results(search_results: list, media_type: Literal['movie','tv']):
    text = ''
    match media_type:
        case 'movie':
            for index,obj in enumerate(search_results[0:10]):
                text += f'[{index + 1}] '+ obj['title'] + ' | ' + obj['release_date'] + '\n'
        case 'tv':
            for index,obj in enumerate(search_results[0:10]):
                text += f'[{index + 1}] '+ obj['name'] + ' | ' + obj['first_air_date'] + '\n'
        case _:
            raise ValueError(f'Wrong media_type: "{media_type}" ! '
            'You can only choose "movie" or "tv".')     
    return text

def run_search(api:str, url:str, media_type: Literal['movie', 'tv']):
    name = input('Movie - TV Show Name:')    
    results = search(url=url, name=name, api=api)
    
    if (len(results) == 0):
        return 'No results found.'
    elif (len(results) == 1):
        index = 0
    else:
        formatted_results = list_results(search_results=results, media_type=media_type)
        print(formatted_results, end='')
        choice = int(input('[0] Exit\n Choose: '))
        if (choice == 0):
            return 'exit'
        index = choice - 1
    data = get_info(media_list=results, media_type=media_type, index=index)
    return (f'''
        =========================
               MOVIE SEARCH
        =========================
        Movie Name: {data['title']}
        Release Date: {data['release_date']}
        iMDB: {data['average_vote']}
        Overview:
        {data['overview']}''')

def get_popular(media_type: Literal['movie','tv']):
    pass

def main(api:str, mov_url:str, tv_url:str):
    subprocess.call('clear')
    choice = input("""
    ======================
          tMDB Search
    ======================
    POPULAR MOVIES:
    ======================
    POPULAR TV SHOWS:
    ======================
    [1] - Search a Movie
    [2] - Search a TV Show
    Press anything else for quit...
    >>>  """)
    if (choice == '1'):
        result = run_search(api=api, url=mov_url, media_type='movie')
    elif (choice == '2'):
        result = run_search(api=api, url=tv_url, media_type='tv')
    else:
        return 'exit'
    return result

load_dotenv()
API = os.getenv('API')

if not API:
    print('No API keys found.')
    exit()

MOVIE_URL = 'https://api.themoviedb.org/3/search/movie'
TV_URL = 'https://api.themoviedb.org/3/search/tv'

while True:
    try:
        result = main(api=API, mov_url=MOVIE_URL, tv_url=TV_URL)
        if (result == 'exit'):
            print('Goodbye!')
            break
        else:
            print(result)
    except (IndexError, ValueError):
        print("Invalid input. Please enter a number from the list.")
    input('Press ENTER to continue...')
