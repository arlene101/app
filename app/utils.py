import requests

class Token():

    def get_token():
        url = "http://hakaton-idp.gov4c.kz/auth/realms/con-web/protocol/openid-connect/token"
        data = {
            "username": "test-operator",
            "password": "DjrsmA9RMXRl",
            "client_id": "cw-queue-service",
            "grant_type": "password"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url, data=data, headers=headers)
        print(response.json().get("access_token"))