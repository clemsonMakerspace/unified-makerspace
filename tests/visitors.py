import requests as r

url = "https://9bhfui3vn2.execute-api.us-east-1.amazonaws.com/api/visitors"
res = r.put(url, json = {

    "hardware_id": "902100",
    "visitor":
    {
        "degree_type": "Phd",
        "email": "joe3@makerspace.com",
        "first_name": "Joe",
        "last_name": "Goldberg",
        "major": "Computer Science",
        "password": "password"
    }
})
print(res.json())