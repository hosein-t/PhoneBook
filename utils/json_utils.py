import json



def read_json(file):
    with open(file, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def write_json(dictionary, file):
    with open(file, "w", encoding="utf-8") as json_file:
        json.dump(dictionary, json_file, ensure_ascii=False, indent=4)
