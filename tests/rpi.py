import requests as r
import json

################################################################################
# SIGNIN TESTING

# request test for signin lambda where user is in Visitor Table and
# successfully adds visitor to Visit Table


def test_signin_visitor_in_DB_hardwareID220722_locationTest_equals_200():
    url = "https://3to3t6gjwa.execute-api.us-east-1.amazonaws.com/iot/signin"

    res = r.post(url, json={
        "HardwareID": "220722",
        "LoginLocation": "Test"
    })

    res_body = res.json()
    print(res.status_code)

    assert res.status_code == 200

# request test for signin lambda where user is not in Visitor Table and
# returns error code 402


def test_signin_visitor_is_not_in_DB_hardwareID000000_locationTest_equals_402():
    url = "https://3to3t6gjwa.execute-api.us-east-1.amazonaws.com/iot/signin"

    res = r.post(url, json={
        "HardwareID": "000000",
        "LoginLocation": "Test"
    })

    res_body = res.json()
    print(res.status_code)

    assert res.status_code == 402

################################################################################
# SIGNOUT TESTING

# request test for signout lambda where user is in Visitor Table and
# successfully adds signout time to visitor in Visit Table


def test_signout_visitor_in_DB_hardwareID220722_equals_200():
    url = "https://3to3t6gjwa.execute-api.us-east-1.amazonaws.com/iot/signout"

    res = r.post(url, json={
        "HardwareID": "220722"
    })

    res_body = res.json()
    print(res.status_code)

    assert res.status_code == 200

# request test for signout lambda where user is not in Visitor Table and
# returns error code 402


def test_signout_visitor_not_in_DB_hardwareID000000_equals_402():
    url = "https://3to3t6gjwa.execute-api.us-east-1.amazonaws.com/iot/signout"

    res = r.post(url, json={
        "HardwareID": "000000"
    })

    res_body = res.json()
    print(res.status_code)

    assert res.status_code == 402


# Can either run with main as python3 rpi.py
# Or run with pytest as pytest rpi.py
if __name__ == "__main__":
    test_signin_visitor_in_DB_hardwareID220722_locationTest_equals_200()
    test_signin_visitor_is_not_in_DB_hardwareID000000_locationTest_equals_402()
    test_signout_visitor_in_DB_hardwareID220722_equals_200()
    test_signout_visitor_not_in_DB_hardwareID000000_equals_402()
