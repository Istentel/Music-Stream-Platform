from flask import  jsonify
import requests, json
from requests.auth import HTTPBasicAuth

headers={
        'Content-type':'application/json', 
        'Accept':'application/json'
        }

def register_user_api(new_user: dict):
    response = requests.post('http://auth_service:5001/register', headers=headers, json=json.dumps(new_user))

    return response
        
def login_user_api(user: str, password: str):

    auth = HTTPBasicAuth(user, password)

    try:
        response = requests.get('http://auth_service:5001/login', auth=auth)
    except Exception as err:
        print(err)
    
    return response

#VALIDATE
def validate_request(request):
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)
    
    token = request.headers["Authorization"]

    if not token:
        return None, ("missing credentials", 401)

    response = requests.post(
        f"http://auth_service:5001/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)


#VALIDATE
def validate_token(token):
    if not token:
        return None, ("missing credentials", 401)

    response = requests.post("http://auth_service:5001/validate", json={'token': token})

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

    
