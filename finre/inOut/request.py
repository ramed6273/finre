import requests

url = 'http://127.0.0.1:8000/add/'

objects = {
    'financial' :   'income',
    'amount'    :   120,
    'title'     :   'abrarvan',
}

request = requests.post(url, data=objects)
