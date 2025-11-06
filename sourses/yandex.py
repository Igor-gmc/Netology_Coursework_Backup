# класс для работы с Yandex

import requests
class YandexAPI:
    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
    BASE_URL_UPLOAD_FILES = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    def __init__(self, api_key: str):
        self.__api_key = api_key

    @property
    def api_key(self):
        return self.__api_key

    def create_folder(self, in_path_folder_breed: str) -> str:
        """
        Создает папку на яндекс диске
        Предварительно проверяет наличие такой папки, чтобы не пересоздавать папку еще раз

        Args:
            path_folder (str): Наименование папки, которую создадим в яндекс диске

        Returns:
            str: Путь для загрузки файлов на яндекс диск
        """

        headers = {"Authorization": f"OAuth {self.api_key}"}

        # Создаем папку для курсовой
        path_hw_folder = "course_paper_ntlg"
        params_hw_folder = {"path": path_hw_folder}
        try:
            resp_hw_folder = requests.put(f"{self.BASE_URL}", headers=headers, params=params_hw_folder)
            if resp_hw_folder.status_code == 201 or resp_hw_folder.status_code == 409:
                print(f"Главная папка создана: {params_hw_folder}, {resp_hw_folder.status_code}")
        except requests.exceptions.Timeout:
            print("Время ожидания ответа истекло: {path_hw_folder}")
            return ""
        except requests.exceptions.ConnectionError:
            print("Ошибка соединения с сервером")
            return ""
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return ""

        # создаем папку для фото породы/подпороды
        try:
            breed_params = {"path": f"{path_hw_folder}/{in_path_folder_breed}"}
            resp_breed_folder = requests.put(self.BASE_URL, headers=headers, params=breed_params)
            if resp_breed_folder.status_code in (200, 201, 202, 409):
                print(f"Папка {path_hw_folder}/{in_path_folder_breed} создана!")
                return f"{path_hw_folder}/{in_path_folder_breed}"
            else:
                return ""
            
        except requests.exceptions.Timeout:
            print("Время ожидания ответа истекло: {path_hw_folder}")
            return ""
        except requests.exceptions.ConnectionError:
            print("Ошибка соединения с сервером")
            return ""
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
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

        

        headers = {"Authorization": f"OAuth {self.api_key}"}

        # Создаем нужную папку для сохранения файлов
        breed_folder = self.create_folder(in_path_folder_breed)
        
        if not breed_folder:
            print("Не удалось создать папку для загрузки")
            return False
        
        # Загружем файлы в созданную папку
        success = True  # флаг для отслеживания неудачных загрузок
    
        for file_name, img_url in file_info:
            path_ = f"{breed_folder}/{file_name}"
            params_load = {"path": path_, "url": img_url}
            params_check_file = {"path": path_}

            try:
                # Отправляем запрос на проверку наличия файла
                resp_check_file = requests.get(self.BASE_URL, headers=headers, params=params_check_file, timeout=10)
                
                # Смотрим есть ли уже такой файл на диске?
                if resp_check_file.status_code == 200: # Если статус 200, то пропускаем загрузку файла
                    print(f"Файл : {file_name} уже есть на диске")
                    continue
                
                # Загружаем файл на диск по ссылке
                resp_upload_yd = requests.post(self.BASE_URL_UPLOAD_FILES, headers=headers, params=params_load, timeout=10)
                
                # Проверяем загрузку файла
                if resp_upload_yd.status_code in (200, 202):
                    print(f"Загружен файл: {file_name}")
                    success = True
                else:
                    print(f"Ошибка {resp_upload_yd.status_code} при загрузке {file_name}: {resp_upload_yd.text}")
                    success = False
                
            except requests.exceptions.Timeout:
                print("Время ожидания ответа истекло")
                success = False
            except requests.exceptions.ConnectionError:
                print("Ошибка соединения с сервером")
                success = False
            except requests.exceptions.RequestException as e:
                print(f"Ошибка запроса: {e}")
                success = False

        if success:
            print("Все файлы успешно загружены!")
        else:
            print("Некоторые файлы не удалось загрузить.")
            
        return success