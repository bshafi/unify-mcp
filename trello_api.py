import httpx
import json
import dotenv
import os

dotenv.load_dotenv()

KEY_TOKEN = {
    'key': os.environ['TRELLO_API_KEY'],
    'token': os.environ['TRELLO_API_TOKEN']
}

BOARD_ID = os.environ['TRELLO_BOARD_ID']

# Use a single client for all requests to improve performance
client = httpx.AsyncClient(timeout=30.0) # Set a reasonable timeout

async def get_lists(board_id):
    """Retrieves a list of all lists in a board"""
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    headers = {"Accept": "application/json"}
    query = {**KEY_TOKEN}

    response = await client.get(url, headers=headers, params=query)

    try:
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError) as e:
        print(f"Error getting lists: {e}")
        return response.text

async def create_card_in_list(list_id, name, description=None):
    """Creates a card in a list"""
    url = "https://api.trello.com/1/cards"
    headers = {"Accept": "application/json"}
    query = {
        'name': name,
        'idList': list_id,
        'desc': description,
        **KEY_TOKEN
    }

    response = await client.post(url, headers=headers, params=query)
    
    try:
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError) as e:
        print(f"Error creating card: {e}")
        return response.text


async def get_cards(board_id):
    """Retrieves a list of all cards in a board"""
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    headers = {"Accept": "application/json"}
    query = {**KEY_TOKEN}
    
    response = await client.get(url, headers=headers, params=query)

    try:
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError):
         # If it fails or is empty, return an empty list
        return []

async def update_card_list(card_id, list_id):
    """Moves a card to a different list"""
    url = f"https://api.trello.com/1/cards/{card_id}"
    headers = {"Accept": "application/json"}
    query = {
        'idList': list_id,
        **KEY_TOKEN
    }
    
    response = await client.put(url, headers=headers, params=query)

    try:
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError) as e:
        print(f"Error updating card list: {e}")
        return None
    
async def get_members(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/members"

    headers = {"Accept": "application/json"}
    query = {
        **KEY_TOKEN
    }
    response = await client.get(url, headers=headers, params=query)

    try:
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError):
         # If it fails or is empty, return an empty list
        return []

async def get_card_members(card_id):
    url = f"https://api.trello.com/1/cards/{card_id}/members"
    query = {
        **KEY_TOKEN
    }
    response = await client.get(url, params=query)

    try:
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError):
         # If it fails or is empty, return an empty list
        return []
    
    
async def assign_card(card_id, member_id):
    url = f"https://api.trello.com/1/cards/{card_id}/idMembers"
    query = {
        'value': member_id,
        **KEY_TOKEN
    }

    response = await client.post(
        url,
        params=query
    )

    try:
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError) as e:
        print(f"Error assigning task: {e}")
        return None

async def remove_card_assignment(card_id, member_id):
    
    url = f"https://api.trello.com/1/cards/{card_id}/idMembers/{member_id}"
    
    params = {
        **KEY_TOKEN
    }

    response = await client.delete(url, params=params)
    try:
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError) as e:
        print(f"Error assigning task: {e}")
        return None
