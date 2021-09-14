import requests as r

url = "https://9bhfui3vn2.execute-api.us-east-1.amazonaws.com/api/tasks"
# CREATE Tasks
res = r.put(url, json={

    # "hardware_id": "902100",
    "tasks":
    {
        "assigned_to": "Bobby",
        "date_created": 1618918223,
        "date_resolved": 1618925456,
        "description": "N/A",
        "status": "Completed",
        "tags": [
            "*"
        ],
        "task_id": "1873480",
        "task_name": "Install new CNC-Router"
    }
})
print(res.json())

# GET Tasks
res = r.post(url, json={
    "start_time": 0,
    "end_time": 9999999999
})
print(res.json())
