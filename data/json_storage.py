import json as js
import os

class JSONStore:
    def __init__(self, path: str):
        self.__path = path
        self.__data_template = {
            "products": [], 
            "last_id": 0
            }
        
        if self.__file_exists() == False:
            self.__create_file()

    def load_data(self) -> str:
        text = ""
        with open(self.__path, "r", encoding='utf-8') as f:
            text = f.read()

        return js.loads(text)

    def save_data(self, new_data: dict):
        with open(self.__path, "w", encoding='utf-8') as f:
            js.dump(new_data, f)

    def __file_exists(self) -> bool:
        return os.path.exists(self.__path)

    def __create_file(self):
        with open(self.__path, "w", encoding='utf-8') as f:
            js.dump(self.__data_template, f)
