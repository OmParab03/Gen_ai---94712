import requests
import json
url="https://jsonplaceholder.typicode.com/users"

response=requests.get(url)

data=response.json()
print(response.status_code)
print("name :", data[1]['name']," email :", data[2]['email'],"phone :", data[1]['phone'],"company name :", data[1]['company']['name'])

user=[
    {"name": data[1]['name']},
    {"email": data[1]['email']},
    {"phone": data[1]['phone']},
    {"company name": data[1]['company']['name']}
    ]

with open('data.json', 'w') as f:
    json.dump(user, f, indent=4)