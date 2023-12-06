import json
import time


def read_json_data(file) -> list:
    with open(file, encoding="utf8") as f:
        return json.load(f)


def write_json_data(file, data: dict) -> list:
    with open(file, mode='w', encoding="utf8") as f:
        f.write(json.dumps(data))


def awaiter(duration, func, *args):
    
    """Функция блокировки выполнения func на duration"""
    time.sleep(duration)
    return func(*args)
