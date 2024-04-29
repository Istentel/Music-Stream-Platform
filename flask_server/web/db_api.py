from flask import  jsonify
import requests, json
from requests.auth import HTTPBasicAuth

headers={
        'Content-type':'application/json', 
        'Accept':'application/json'
        }

def register_user_api(new_user: dict):
    response = requests.post('http://auth_service:5001/api/register', headers=headers, json=json.dumps(new_user))

    if response:
        return response.content, response.status_code
    else:
        return jsonify({'message': 'No valid response'})
        
def login_user_api(user: str, password: str):

    auth = HTTPBasicAuth(user, password)

    response = requests.get('http://auth_service:5001/api/login', auth=auth)

    return response