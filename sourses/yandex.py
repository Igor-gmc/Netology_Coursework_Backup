# класс для работы с Yandex

import requests

class Yandex:
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

        base_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = {"Authorization": f"OAuth {self.api_key}"}

        # Создаем папку для курсовой
        path_hw_folder = "course_paper_ntlg"
        params_hw_folder = {"path": path_hw_folder}
        try:
            resp_hw_folder = requests.put(f"{base_url}", headers=headers, params=params_hw_folder)
            if resp_hw_folder.status_code != 201 or resp_hw_folder.status_code != 409:
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

        # создаем папку для фото породы/подпороды
        try:
            breed_params = {"path": f"{path_hw_folder}/{in_path_folder_breed}"}
            resp_breed_folder = requests.put(base_url, headers=headers, params=breed_params)
            if resp_breed_folder.status_code != 201 or resp_breed_folder.status_code != 409:
                return ""
            return f"{path_hw_folder}/{in_path_folder_breed}"
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

        base_url_upload_files = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = {"Authorization": f"OAuth {self.api_key}"}

        # Создаем нужную папку для сохранения файлов
        breed_folder = self.create_folder(in_path_folder_breed)
        
        if not breed_folder:
            print("Не удалось создать папку для загрузки")
            return False
        
        # Загружем файлы в созданную папку
        success = True  # флаг для отслеживания неудачных загрузок
    
        for file_name, img_url in file_info:
            params = {"path": f"{breed_folder}/{file_name}", "url": img_url}
            try:
                resp_upload_yd = requests.post(base_url_upload_files, headers=headers, params=params, timeout=10)
                if resp_upload_yd.status_code in (200, 202):
                    print(f"Загружен файл: {file_name}")
                elif resp_upload_yd.status_code == 409:
                    print(f"Файл уже существует: {file_name}")
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

        return success
        
        