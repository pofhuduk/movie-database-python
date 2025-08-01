import requests
import dotenv
import os

dotenv.load_dotenv()
API = os.getenv('API')

r = requests.get('https://api.themoviedb.org/3/discover/movie', params= {'api_key': API}).json()

pop1 =r['results'][0]
print(pop1)
