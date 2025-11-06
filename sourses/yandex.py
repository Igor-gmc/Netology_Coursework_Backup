# класс для работы с Yandex

import requests
import logging
from logging.handlers import RotatingFileHandler
import os
class YandexAPI:
    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
    BASE_URL_UPLOAD_FILES = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    def __init__(self, api_key: str):
        self.__api_key = api_key

        # Логгер
        os.makedirs("logs", exist_ok=True)  # создаём папку logs при необходимости
        self.logger = logging.getLogger("YandexAPI")
        self.logger.setLevel(logging.INFO)

        # чтобы не дублировались сообщения при многократном создании экземпляров
        if not self.logger.handlers:
            # формат вывода
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

            # обработчик для файла (максимум 10 МБ, хранить 3 файла)
            file_handler = RotatingFileHandler("logs/yandex_api.log", maxBytes=10_000_000, backupCount=3, encoding="utf-8")
            file_handler.setFormatter(formatter)

            # обработчик для консоли
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            # добавляем обработчики
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    @property
    def api_key(self):
        return self.__api_key
    
    @property
    def headers_prop(self):
        return {"Authorization": f"OAuth {self.api_key}"}

    def create_folder(self, in_path_folder_breed: str) -> str:
        """
        Создает папку на яндекс диске
        Предварительно проверяет наличие такой папки, чтобы не пересоздавать папку еще раз

        Args:
            path_folder (str): Наименование папки, которую создадим в яндекс диске

        Returns:
            str: Путь для загрузки файлов на яндекс диск
        """

        #headers = {"Authorization": f"OAuth {self.api_key}"}

        # Создаем папку для курсовой
        path_hw_folder = "course_paper_ntlg"
        params_hw_folder = {"path": path_hw_folder}
        try:
            resp_hw_folder = requests.put(f"{self.BASE_URL}", headers=self.headers_prop, params=params_hw_folder)
            if resp_hw_folder.status_code == 201 or resp_hw_folder.status_code == 409:
                # print(f"Главная папка создана: {params_hw_folder}, {resp_hw_folder.status_code}")
                self.logger.info(f"Главная папка создана: {params_hw_folder}, {resp_hw_folder.status_code}")
        
        # вывести все в декоратор, но не получилось, ломается больше чем чинится, поэтому оставил повторяющийся код
        except requests.exceptions.Timeout:
            # print("Время ожидания ответа истекло: {path_hw_folder}")
            self.logger.error("Время ожидания ответа истекло: {path_hw_folder}")
            return ""
        except requests.exceptions.ConnectionError:
            # print("Ошибка соединения с сервером")
            self.logger.error("Ошибка соединения с сервером")
            return ""
        except requests.exceptions.RequestException as e:
            # print(f"Ошибка запроса: {e}")
            self.logger.error(f"Ошибка запроса: {e}")
            return ""

        # создаем папку для фото породы/подпороды
        try:
            breed_params = {"path": f"{path_hw_folder}/{in_path_folder_breed}"}
            resp_breed_folder = requests.put(self.BASE_URL, headers=self.headers_prop, params=breed_params)
            if resp_breed_folder.status_code in (200, 201, 202, 409):
                # print(f"Папка {path_hw_folder}/{in_path_folder_breed} создана!")
                self.logger.info(f"Папка {path_hw_folder}/{in_path_folder_breed} создана!")
                return f"{path_hw_folder}/{in_path_folder_breed}"
            else:
                self.logger.error("Ошибка: Папка {path_hw_folder}/{in_path_folder_breed} не создана!!!")
                return ""

        # вывести все в декоратор, но не получилось, ломается больше чем чинится, поэтому оставил повторяющийся код     
        except requests.exceptions.Timeout:
            # print("Время ожидания ответа истекло: {path_hw_folder}")
            self.logger.error("Время ожидания ответа истекло: {path_hw_folder}")
            return ""
        except requests.exceptions.ConnectionError:
            # print("Ошибка соединения с сервером")
            self.logger.error("Ошибка соединения с сервером")
            return ""
        except requests.exceptions.RequestException as e:
            # print(f"Ошибка запроса: {e}")
            self.logger.error(f"Ошибка запроса: {e}")
            return ""        

    def load_files_to_yd(self,
                         in_path_folder_breed: str,     # Название папки для сохранения фоток породы
                         file_info: list[list]          # file_name, img_url
                         ) -> bool:
        """
        Загружает файлы на яндекс диск, по указанному пути

        Args:
            in_path_folder_breed: str,      # Название папки для сохранения фоток породы
            file_info: list[list]           # file_name - название для сохранения файла, img_url - ссылка на скачивание файла

        Returns:
            bool: Если файлы загружены, то возвращается True, иначе False
        """

        

        #headers = {"Authorization": f"OAuth {self.api_key}"}

        # Создаем нужную папку для сохранения файлов
        breed_folder = self.create_folder(in_path_folder_breed)
        
        if not breed_folder:
            # print("Не удалось создать папку для загрузки")
            self.logger.warning("Не удалось создать папку для загрузки: self.create_folder(in_path_folder_breed)")
            return False
        
        # Загружем файлы в созданную папку
        success = True  # флаг для отслеживания неудачных загрузок
    
        for file_name, img_url in file_info:
            path_ = f"{breed_folder}/{file_name}"
            params_load = {"path": path_, "url": img_url}
            params_check_file = {"path": path_}

            try:
                # Отправляем запрос на проверку наличия файла
                resp_check_file = requests.get(self.BASE_URL, headers=self.headers_prop, params=params_check_file, timeout=10)
                
                # Смотрим есть ли уже такой файл на диске?
                if resp_check_file.status_code == 200: # Если статус 200, то пропускаем загрузку файла
                    # print(f"Файл : {file_name} уже есть на диске")
                    self.logger.warning(f"Файл : {file_name} уже есть на диске")
                    continue
                
                # Загружаем файл на диск по ссылке
                resp_upload_yd = requests.post(self.BASE_URL_UPLOAD_FILES, headers=self.headers_prop, params=params_load, timeout=10)
                
                # Проверяем загрузку файла
                if resp_upload_yd.status_code in (200, 202):
                    # print(f"Загружен файл: {file_name}")
                    self.logger.info(f"Загружен файл: {file_name}")
                    success = True
                else:
                    # print(f"Ошибка {resp_upload_yd.status_code} при загрузке {file_name}: {resp_upload_yd.text}")
                    self.logger.error(f"Ошибка {resp_upload_yd.status_code} при загрузке {file_name}: {resp_upload_yd.text}")
                    success = False

            # вывести все в декоратор, но не получилось, ломается больше чем чинится, поэтому оставил повторяющийся код    
            except requests.exceptions.Timeout:
                # print("Время ожидания ответа истекло")
                self.logger.error("Время ожидания ответа истекло")
                success = False
            except requests.exceptions.ConnectionError:
                # print("Ошибка соединения с сервером")
                self.logger.error("Ошибка соединения с сервером")
                success = False
            except requests.exceptions.RequestException as e:
                # print(f"Ошибка запроса: {e}")
                self.logger.error(f"Ошибка запроса: {e}")
                success = False

        if success:
            # print("Все файлы успешно загружены!")
            self.logger.info("Все файлы успешно загружены!")
        else:
            # print("Некоторые файлы не удалось загрузить.")
            self.logger.warning("Некоторые файлы не удалось загрузить.")

        return success