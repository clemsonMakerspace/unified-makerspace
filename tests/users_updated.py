import requests as r
import json

url = 'https://9bhfui3vn2.execute-api.us-east-1.amazonaws.com'

body = {
'email': "joe@makerspace.com",
'first_name': "joe",
'last_name': "goldberg",
'password': "password",
'user_token': "123456789"
}


res  = r.put(f'{url}/api/users', json.dumps(body))

print(res)
print(res.text)
print(res.json())
