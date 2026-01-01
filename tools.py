from datetime import datetime
import json
import os

def today() -> datetime:
    return datetime.now()

class ObjCheck:

    def __init__(self, obj) -> None:
        self.obj = obj

    def length(self, size: int):
        if len(self.obj) != size:
            raise ValueError(f"Lenght of {self.obj} ({len(self.obj)}) different than the desired of {size}.")
        else:
            return self.obj

    def max_length(self, size: int):
        if len(self.obj) > size:
            raise ValueError(f"Lenght of {self.obj} ({len(self.obj)}) higher than the desired of {size}.")
        else:
            return self.obj

    def options(self, options_list: list[object]):
        if self.obj in options_list:
            return self.obj
        else:
            raise ValueError(f"Object {self.obj} isn't a valid option. Valid options: \n{options_list}")

class FilesManagers:

    @staticmethod
    def get_json(path: str):
        with open(path, 'r', encoding='utf-8') as f:
            x = json.load(f)
            return x
        
    @staticmethod
    def save_json(path: str, data: dict) -> str:
        with open('_temp.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace('_temp.json', path)
        return 'File recorded with success.'

    @staticmethod
    def select_years(open_dt: str, close_dt: str) -> list[int]:
        x = []
        open_dt_year = datetime.fromisoformat(open_dt).year
        close_dt_year = datetime.fromisoformat(close_dt).year
        while open_dt_year <= close_dt_year:
            x += [open_dt_year]
            open_dt_year += 1
        return x
    
def format_value(value: float, positive: bool) -> str:
    if positive:
        return f"{value:,.2f}" if value >= 0 else f"({-value:,.2f})"
    else:
        return f"({value:,.2f})" if value >= 0 else f"{-value:,.2f}"
