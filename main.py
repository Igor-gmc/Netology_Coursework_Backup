from pprint import pprint
from sourses import dogs  # убедись, что dogs.py находится в папке sourses и содержит класс DogAPI

api = dogs.DogAPI("hound")
breed_list = api.search_breed()
data = api.get_breed_dict(breed_list)

pprint(data)