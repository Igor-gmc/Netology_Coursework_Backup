from pprint import pprint
from sourses import dogs  # убедись, что dogs.py находится в папке sourses и содержит класс DogAPI

# Получаем словарь с данными для скачивания
# {breed_folder: [file_name , url_file_name_image]
api_dog = dogs.DogAPI("hound")                  # создаем экземпляр класса DogAPI
breed_list = api_dog.search_breed()             # формируем список пород/подпород
data = api_dog.get_breed_dict(breed_list)       # формируем словарь {breed_folder: [file_name , url_file_name_image]
pprint(data)

# Записываем информацию  на яндекс диск

