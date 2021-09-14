import requests as r
import json

url = "https://9bhfui3vn2.execute-api.us-east-1.amazonaws.com/api/users"

# CREATE USER
# Must generate a user token from administration to test


def create_user_success():
    res = r.put(url, json={
        "email": "New.Example.test@emailaddress.com",
        "password": "Password123",
        "first_name": "My",
        "last_name": "Name",
        "user_token": "4lT+h10="
    })
    request_body = res.json()
    print("Create success user : ", request_body["user"])
    print("Create success token : ", request_body["auth_token"])
    assert request_body["statusCode"] == 200


def create_user_wrong_token():
    res = r.put(url, json={
        "email": "Example.test@emailaddress.com",
        "password": "Password123",
        "first_name": "My",
        "last_name": "Name",
        "user_token": "not-a-token"
    })
    request_body = res.json()
    print("Wrong token messaeg: ", request_body["message"])
    assert (request_body["statusCode"] ==
            405 or request_body["statusCode"] == 206)

# Also requires a valid token from administration to test


def create_user_email_in_use():
    res = r.put(url, json={
        "email": "Example.test@emailaddress.com",
        "password": "Password123",
        "first_name": "My",
        "last_name": "Name",
        "user_token": "ZV2/QZI="
    })
    request_body = res.json()
    print("Email in use message: ", request_body["message"])
    assert request_body["statusCode"] == 400


if __name__ == "__main__":
    create_user_success()
    create_user_wrong_token()
    create_user_email_in_use()
