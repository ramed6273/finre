import requests

url = 'http://127.0.0.1:8000/add/'

objects = {
    'financial' :   'expense',
    'amount'    :   15,
    'title'     :   'adams nooshabe',
}

request = requests.post(url, data=objects)