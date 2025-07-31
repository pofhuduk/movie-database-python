import requests
import os
from dotenv import load_dotenv
import subprocess

def search_movie(url:str, api:str, movie_name:str):
    params = {
            'query': movie_name,
            'api_key': api
            }
    r = requests.get(url, params=params).json()
    results = r['results']
    
    return results

def get_movie(json:list, index:int):
    movie = json[index]

    title = movie['title']
    overview = movie['overview']
    release_date = movie['release_date']
    vote_average = movie['vote_average']
    vote_formatted = str(vote_average)[0:3]
    
    return title, release_date, vote_formatted, overview

def main(api:str, url:str):
    subprocess.call('clear')
    movie_name = input('Movie Name:')
    
    results = search_movie(url=url, movie_name=movie_name, api=api)

    if (len(results) == 1):
        index = 0
    elif (len(results) == 0):
        print("No results found.")
        return 0
    else:
        text = ''
        for index,obj in enumerate(results[0:10]):
            text += f'[{index + 1}] '+ obj['title'] + ' | ' + obj['release_date'] + '\n'
        choice = input(text + 'Choose:')
        index = int(choice) - 1

    title, release_date, vote, overview = get_movie(json=results, index=index)

    print(f'''
        =========================
               MOVIE SEARCH
        =========================
        Movie Name: {title}
        Release Date: {release_date}
        iMDB: {vote}
        Overview:
        {overview}''')


load_dotenv()
API = os.getenv('API')

if not API:
    print('No API keys found.')
    exit()

URL = 'https://api.themoviedb.org/3/search/movie'

while True:
    try:
        main(api=API, url=URL)
    except (IndexError, ValueError):
        print("Invalid input. Please enter a number from the list.")
    input('Press ENTER to continue...')
