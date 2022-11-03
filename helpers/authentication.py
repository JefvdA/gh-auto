"""
This file contains methods for authenticating users.
"""

import os
import json
dir = os.path.dirname(__file__)


Path = os.path.join(dir, '../secrets.json')


def get_token():
    """
    This method returns authentication the token for the current user.
    """
    try:
        with open(Path, 'r') as f:
            data = json.load(f)
            try:
                return data['authentication-token']
            except KeyError:
                return set_token()
    except FileNotFoundError:
        return set_token()


def set_token():
    """
    This method asks the authentication token for the current user, and stores it for future use.
    """
    print("Authentication token not found. Please authenticate before continuing...")
    print("For more information, please visit our documentation at https://github.com/JefvdA/gh-auto")

    token = input("Please enter your github authentication token: ")
    entry = { 'authentication-token': token }

    try:
        with open(Path, 'r') as f:
            data = json.load(f)
            data.update(entry)
    except FileNotFoundError:
        data = entry

    with open(Path, 'w') as f:
        json.dump(data, f)

    return token