import requests
import os
from dotenv import load_dotenv
import subprocess

def search(url:str, api:str, name:str):
    params = {
            'query': name,
            'api_key': api
            }
    r = requests.get(url, params=params).json()
    results = r['results']
    
    return results

def get_movie(movie_list:list, index:int):
    movie = movie_list[index]

    title = movie['title']
    overview = movie['overview']
    release_date = movie['release_date']
    vote_average = movie['vote_average']
    vote_formatted = str(vote_average)[0:3]
    
    return {
            'title': title,
            'overview': overview,
            'release_date': release_date,
            'average_vote': vote_formatted
            }

def get_tv(tv_list:list, index:int):
    show = tv_list[index]

    name = show['name']
    overview = show['overview']
    first_air_date = show['first_air_date']
    vote_average = show['vote_average']
    vote_formatted = str(vote_average)[0:3]
    
    return {
            'name': name,
            'overview': overview,
            'first_air_date': first_air_date,
            'average_vote': vote_formatted
            }

def run_movie_search(api:str, url:str):
    movie_name = input('Movie Name:')    
    results = search(url=url, name=movie_name, api=api)

    if (len(results) == 1):
        index = 0
    elif (len(results) == 0):
        print("No results found.")
        return 0
    else:
        text = ''
        for index,obj in enumerate(results[0:10]):
            text += f'[{index + 1}] '+ obj['title'] + ' | ' + obj['release_date'] + '\n'
        text += '[0] Exit\n'
        choice = input(text + 'Choose:')
        
        if (choice == '0'):
            print('Goodbye!')
            return 'exit'
        index = int(choice) - 1
        
    movie_data = get_movie(movie_list=results, index=index)

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
        print("No results found.")
        return 0
    else:
        text = ''
        for index,obj in enumerate(results[0:10]):
            text += f'[{index + 1}] '+ obj['name'] + ' | ' + obj['first_air_date'] + '\n'
        text += '[0] Exit\n'
        choice = input(text + 'Choose:')
        
        if (choice == '0'):
            print('Goodbye!')
            return 'exit'
        index = int(choice) - 1
        
    tv_data = get_tv(tv_list=results, index=index)

    return (f'''
        =========================
                SHOW SEARCH
        =========================
        Movie Name: {tv_data['name']}
        Release Date: {tv_data['first_air_date']}
        iMDB: {tv_data['average_vote']}
        Overview:
        {tv_data['overview']}''')

def main(api:str, mov_url:str, tv_url:str):
    subprocess.call('clear')
    x = input('1 - Movie Search | 2 - TV Show Search')
    if (x == '1'):
        result = run_movie_search(api=api, url=mov_url)
    elif (x == '2'):
        result = run_tv_search(api=api, url=tv_url)
    else:
        result = None

    print(result)

load_dotenv()
API = os.getenv('API')

if not API:
    print('No API keys found.')
    exit()

MOVIE_URL = 'https://api.themoviedb.org/3/search/movie'
TV_URL = 'https://api.themoviedb.org/3/search/tv'

while True:
    try:
        main(api=API, mov_url=MOVIE_URL, tv_url=TV_URL)
    except (IndexError, ValueError):
        print("Invalid input. Please enter a number from the list.")
    input('Press ENTER to continue...')

