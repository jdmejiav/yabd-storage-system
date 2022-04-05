import json

def save(data:dict,name):
    with open(f'{name}.json', 'w') as fp:
        json.dump(data, fp)

def get(name):
    with open(f'{name}.json') as json_file:
        data = json.load(json_file)
        return data
def file_exists(name):
    try:
        file= open(f'{name}.json')
        return True
    except:
        return False
