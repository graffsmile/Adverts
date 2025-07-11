import requests


params_user = {
    'user_name': 'Davy Jones',
    # 'password': 'vdsvkvj',
}

params = {
    'tittle': 'Летучий Голландец',
    'description': 'Продается корабль, не бит, не крашен, без пробега по Черному морю',
    'owner': 3,
}

patch_params = {
    'description': 'Продается машина без пробега по уралу',
}

# r = requests.get('http://localhost:5000/adverts/1')
# r = requests.get('http://localhost:5000/user/1')

# r = requests.post('http://localhost:5000/user/', json=params_user)
# r = requests.post('http://localhost:5000/adverts/', json=params)

# r = requests.delete('http://localhost:5000/adverts/3')
r = requests.patch('http://localhost:5000/adverts/1', json=patch_params)

print(r)
print(r.json())
# if r.ok:
#     print(r.json())