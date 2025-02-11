import requests

api_key = ""
app_key = ""
role_assigned = ""
role_revoke = ""


headers = {
    'Accept': 'application/json',
    'DD-API-KEY': api_key,
    'DD-APPLICATION-KEY': app_key,
    'Content-Type': 'application/json'
}

def get_user_id():

    # Listing users
    url = f"https://api.datadoghq.com/api/v2/users?filter=Datadog%20Standard%20Role&filter%5Bstatus%5D=Active%2CPending&filter%5Ballowed_login_methods%5D=standard%2Cgoogle_oidc%2CSAML&page%5Bsize%5D=1000&page%5Bnumber%5D=0&sort=name&include=identity_providers%2Callowed_login_methods_identity_providers"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Users found with success!") 
        return response.json()
    else:
        print(f"Error to search users: {response.status_code}\n{response.text}")

def add_role(user_id, handle):
    url = f"https://api.datadoghq.com/api/v2/roles/{role_assigned}/users"
    payload = {
        "data": {
            "id": user_id,
            "type": "users"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"User {handle} role asset with success")
    else:
        print(f"Erro to add role to user {handle}: {response.status_code} - {response.text}")

def del_role(user_id, handle):
    url = f"https://api.datadoghq.com/api/v2/roles/{role_revoke}/users"
    payload = {
        "data": {
            "id": user_id,
            "type": "users"
        }
    }
    response = requests.delete(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"User {handle} role delete with success")
    else:
        print(f"Erro to delete role to user {handle}: status {response.status_code} - {response.text}")


if __name__ == "__main__":
    
    users = get_user_id()
    for user in users["data"]:
        user_id = user["id"]
        handle = user["attributes"]["handle"]

        del_role(user_id, handle)
        add_role(user_id, handle)
        print('*' * 30)
