import json
import os


def view_json(data: dict) -> str:
    return json.dumps(data, indent=4)

def write_json(data: dict, file_path: str) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def load_json(file_path: str,) -> dict:
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)