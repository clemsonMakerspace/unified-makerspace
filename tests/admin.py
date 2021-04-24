import requests as r
import json

url = "https://9bhfui3vn2.execute-api.us-east-1.amazonaws.com/api/administrative"
# GENERATE USER TOKEN
def generate_user_token_success():
    res = r.post(url, json = { })
    request_body = res.json()
    print("Token Generated: ", request_body["user_token"])
    assert request_body["statusCode"] == 200

# RESET PASSWORD
def reset_password_success():
    res = r.patch(url, json = {
        "email": "email.test13@address.com"
    })
    request_body = res.json()
    print(request_body)
    print("Reset password success response: ", request_body["message"])
    assert request_body["statusCode"] == 200

def reset_password_user_does_not_exist():
    res = r.patch(url, json = {
        "email": "fake_user@email.com"
    })
    request_body = res.json()
    print("Reset password fail response: ", request_body["message"])
    assert request_body["statusCode"] == 500

if __name__ == "__main__":
    generate_user_token_success()
    reset_password_success()
    reset_password_user_does_not_exist()
