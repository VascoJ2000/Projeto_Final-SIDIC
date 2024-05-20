
import requests


url = 'http://127.0.0.1:8000'


def login(email, password):
    res = requests.get(url=url+f'/auth/{email}/{password}')
    if res.status_code == 200:
        return res.json()
    return False


def signin(email, password):
    headers = {'Content-Type': 'application/json charset=utf-8'}
    json_data = {
        'email': email,
        'password': password
    }
    res = requests.post(url=url+'/auth', headers=headers, json=json_data)
    if res.status_code == 201:
        return res.json()
    return False


def logout():
    res = requests.delete(url=url+'/auth')
    if res.status_code == 200:
        return res.text
    return False
