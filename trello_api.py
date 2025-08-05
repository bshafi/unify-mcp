# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
import json
import dotenv

dotenv.load_dotenv()
import os

KEY_TOKEN = {
    'key': os.environ['TRELLO_API_KEY'],
    'token': os.environ['TRELLO_API_TOKEN']
}

BOARD_ID = os.environ['TRELLO_BOARD_ID']

def get_lists(board_id):
    "Retrieves a list of all lists in a board"
    url = f"https://api.trello.com/1/boards/{board_id}/lists"

    headers = {
    "Accept": "application/json"
    }

    query = { **KEY_TOKEN }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        timeout=1000
    )

    try:
        return response.json()
    except Exception: # pylint: disable=W0718
        return response.content

def create_card_in_list(list_id, name, description=None):
    "Creates a card in a list"
    url = "https://api.trello.com/1/cards"

    headers = {
        "Accept": "application/json"
    }

    query = {
        'name': name,
        'idList': list_id,
        'desc': description,
        **KEY_TOKEN
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        params=query,
        timeout=1000
    )
    if response.ok:
        return response.json()
    return response.content
