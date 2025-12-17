from datetime import datetime
import json
import os
import core

def years_select(open_dt: str, close_dt: str) -> list[int]:
    x = []
    open_dt = datetime.fromisoformat(open_dt).year
    close_dt = datetime.fromisoformat(close_dt).year
    while open_dt <= close_dt:
        x += [open_dt]
        open_dt += 1
    return x

def get_rootfile() -> core.RootFile:
    with open('_root.json', 'r', encoding='utf-8') as f:
         return core.RootFile(json.load(f))

def get_entriesfiles(years_list: list[int]) -> core.EntriesFile:
    x = {
        'entries': {},
        'open': {}}
    for item in years_list:
        file = os.path.join('entries', f"{item}.json") 
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                x['entries'].update(data['entries'])
                if len(x['open'].keys()) == 0:
                    x['open'].update(data['open'])
    return core.EntriesFile(x)

def savejson(data: object, path: str) -> None:
    with open('_temp.json', 'w', encoding='utf-8') as f:
        json.dump(data.to_dict(), f, indent=4, ensure_ascii=False)
    os.replace('_temp.json', path)
    print('File recorded with success.')
    try:
        os.remove('_temp.json')
    except:
        pass
