from pprint import pprint
from sourses import dogs  # класс DogAPI
from sourses import yandex # класс YndexPI
import os
from dotenv import load_dotenv


# Получаем словарь с данными для скачивания
# {breed_folder: [file_name , url_file_name_image]
api_dog = dogs.DogAPI("hound")                  # создаем экземпляр класса DogAPI
breed_list = api_dog.search_breed()             # формируем список пород/подпород
data_dog = api_dog.get_breed_dict(breed_list)       # формируем словарь {breed_folder: [file_name , url_file_name_image]
pprint(data_dog)

# Создаем экзепляр класса с API доступом ЯндексДиск
load_dotenv()
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
if not YANDEX_API_KEY:
    raise ValueError("Не удалось получить API ключ YANDEX_API_KEY")
lf = yandex.YandexAPI(YANDEX_API_KEY)

# Записываем информацию  на яндекс диск
# Выберем по одному значению из полученной информации о породе/подпороде
for bread_folder, breed_data in data_dog.items():
    print(bread_folder)
    print([breed_data[0]])
    status_load = lf.load_files_to_yd(bread_folder, [breed_data[0]])
