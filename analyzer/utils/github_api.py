import requests

import requests

def get_user_profile(username):
    try:
        response = requests.get(f'https://api.github.com/users/{username}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("GitHub API error:", e)
        return None


def get_user_repos(username):
    response = requests.get(f'https://api.github.com/users/{username}/repos')
    return response.json()