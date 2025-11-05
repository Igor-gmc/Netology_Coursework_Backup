# Класс для работы с dogs API

import requests
class DogAPI:
    base_url = "https://dog.ceo/api/breed/"
    base_image_url = "https://images.dog.ceo/breeds/"

    def __init__(self, breed: str):
        self.breed = breed

    def search_breed(self) ->list:
        """
        Функция проверяет наличие породы в списке пород

        Returns:
            list: спсиок пород
        """
        breed_list = []

        # Отправляем запрос в dogs
        resp_breed = requests.get(f"{self.base_url}{self.breed}/images")

        # Проверяем наличие породы в списке пород
        if not resp_breed.ok:
            print(f"Порода {self.breed} не найдена. Ошибка: 404")
            return breed_list
        
        # Проверяем наличие подпород
        resp_sub_bred = requests.get(f"{self.base_url}{self.breed}/list")
        list_sub_bred = resp_sub_bred.json()["message"] # получаем список подпород
        
        if not list_sub_bred:
            #  если подпород нет, возвращаем список с названием породы
            print(f"У породы {self.breed} отсутствуют подпороды")
            return [self.breed]
        else:
            # если подпороды есть, возвращаем список подпород
            print(f"У породы {self.breed} есть подпорода(ы): {', '.join(list_sub_bred)}")
            return [f"{self.breed}-{sub_bred}" for sub_bred in list_sub_bred]
        
    def get_breed_dict(self, breed_list: list) -> dict:
        """
        Формирует словарь из списка пород

        Args:
            breed_list (list): Список пород

        Returns:
            dict: словарь с описанием данных для последующей обработки
            breed_folder(название папки для сохранения фото породы собаки):
             [file_name = название файла для сохранение картинки breed + file_name.jpg,
              url_file_name_image = ссылка на скачивание]
        """
        
        if not breed_list:
            print("Список пород пустой!")
            return {}
        
        # Формируем словарь с данными о запросе породы
        # получим список картинок по породе
        resp_img = requests.get(f"{self.base_url}{self.breed}/images")
        if not resp_img.ok:
            print(f"Ошибка при получении изображений ({resp_img.status_code})")
            return {}
        images_list = resp_img.json()["message"]

        # соберем словарь с названиями картинок породы/каждой подпороды
        breed_dict = {}
        for breed_name in breed_list:
            # Парсим все картинки на всякий случай
            for img_url in images_list:
                #  извлекаем данные из url
                try:
                    # разбиваем ссылку и пробуем получить имя файла
                    # если не получится, то будет ошибка индекса и перехватим её
                    breed_data = img_url.split("/breeds/", 1)[1].split("/")
                    file_name_url = breed_data[1]                  # Получаем имя файла по ссылке
                    file_name = f"{breed_name}-{file_name_url}"     # Формируем имя файла согласно ТЗ
                    breed_in_url = breed_data[0]                   # Получаем породу по ссылке
                except IndexError as e:
                    print(f"некорректная ссылка\n{img_url}\n{e}")
                    continue
                
                # Записываем в словарь пару Название файла для будущего сохранения, ссылка на файл
                if breed_name == breed_in_url:
                    breed_dict.setdefault(breed_name, []).append([file_name, img_url])
                else:
                    continue
        return breed_dict