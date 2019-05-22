import json
import requests


def parser_json_data():
    params = {
        'key': 'cee97bd462d0cad269813bcd131652f0',
        'num': 10
    }
    resp = requests.get('http://api.tianapi.com/guonei', params)
    data_model = json.loads(resp.text)
    print(data_model)
    print(data_model['code'])
    print(data_model['msg'])


def serialize_json_data():
    data_dict = {
        'name': '骆昊',
        'age': 38,
        'qq': 957658,
        'friends': ['王大锤', '白元芳'],
        'cars': [
            {'brand': 'BYD', 'max_speed': 180},
            {'brand': 'Audi', 'max_speed': 280},
            {'brand': 'Benz', 'max_speed': 320}
        ]
    }

    with open('./data.json', 'w', encoding='utf-8') as fs:
        json.dump(data_dict, fs)


if __name__ == '__main__':
    serialize_json_data()
