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

def run_movie_search(api:str, url:str):
    movie_name = input('Movie Name:')    
    results = search(url=url, name=movie_name, api=api)

    if (len(results) == 1):
        index = 0
    elif (len(results) == 0):
        return "No results found."
    else:
        text = ''
        for index,obj in enumerate(results[0:10]):
            text += f'[{index + 1}] '+ obj['title'] + ' | ' + obj['release_date'] + '\n'
        text += '[0] Exit\n'
        choice = input(text + 'Choose: ')
        
        if (choice == '0'):
            return 'exit'
        index = int(choice) - 1
    try:    
        movie_data = get_info(media_list=results, index=index, media_type='movie')
    except ValueError as e:
        print(e)
        exit()
    return (f'''
        =========================
               MOVIE SEARCH
        =========================
        Movie Name: {movie_data['title']}
        Release Date: {movie_data['release_date']}
        iMDB: {movie_data['average_vote']}
        Overview:
        {movie_data['overview']}''')


def run_tv_search(api:str, url:str):
    tv_name = input('Show Name:')
    results = search(url=url, name=tv_name, api=api)

    if (len(results) == 1):
        index = 0
    elif (len(results) == 0):
        return "No results found."
    else:
        text = ''
        for index,obj in enumerate(results[0:10]):
            text += f'[{index + 1}] '+ obj['name'] + ' | ' + obj['first_air_date'] + '\n'
        text += '[0] Exit\n'
        choice = input(text + 'Choose:')
        
        if (choice == '0'):
            return 'exit'
        index = int(choice) - 1
        
    tv_data = get_info(media_list=results, index=index, media_type='tv')

    return (f'''
        =========================
                SHOW SEARCH
        =========================
        Movie Name: {tv_data['title']}
        Release Date: {tv_data['release_date']}
        iMDB: {tv_data['average_vote']}
        Overview:
        {tv_data['overview']}''')

def main(api:str, mov_url:str, tv_url:str):
    subprocess.call('clear')
    choice = input("""
    ======================
          tMDB Search
    ======================
    [1] - Search a Movie
    [2] - Search a TV Show
    Press anything else for quit...
    >>>  """)
    if (choice == '1'):
        result = run_movie_search(api=api, url=mov_url)
    elif (choice == '2'):
        result = run_tv_search(api=api, url=tv_url)
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
