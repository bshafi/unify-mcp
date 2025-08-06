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

client = httpx.AsyncClient(timeout=30.0)

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

async def update_card_description(card_id, description):
    """Updates the description of a card"""
    url = f"https://api.trello.com/1/cards/{card_id}"
    headers = {"Accept": "application/json"}
    query = {
        'desc': description,
        **KEY_TOKEN
    }
    
    response = await client.put(url, headers=headers, params=query)

    try:
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError) as e:
        print(f"Error updating card description: {e}")
        return None

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

async def get_checklists_on_card(card_id):
    """Retrieves all checklists and their items on a specific card."""
    url = f"https://api.trello.com/1/cards/{card_id}/checklists"
    headers = {"Accept": "application/json"}
    query = {
        'checkItems': 'all',
        **KEY_TOKEN
    }
    response = await client.get(url, headers=headers, params=query)
    try:
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError):
        return []

async def create_checklist(card_id, name):
    """Creates a new checklist on a card, good for a card that encompasses multiple tasks."""
    url = f"https://api.trello.com/1/checklists"
    headers = {"Accept": "application/json"}
    query = {
        'idCard': card_id,
        'name': name,
        **KEY_TOKEN
    }
    response = await client.post(url, headers=headers, params=query)
    try:
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError) as e:
        print(f"Error creating checklist: {e}")
        return response.text

async def create_check_item(checklist_id, name):
    """Adds an item to a checklist."""
    url = f"https://api.trello.com/1/checklists/{checklist_id}/checkItems"
    headers = {"Accept": "application/json"}
    query = {
        'name': name,
        **KEY_TOKEN
    }
    response = await client.post(url, headers=headers, params=query)
    try:
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError) as e:
        print(f"Error creating check item: {e}")
        return response.text

async def update_check_item_state(card_id, check_item_id, is_complete: bool):
    """Updates the state of a check item (complete/incomplete)."""
    url = f"https://api.trello.com/1/cards/{card_id}/checkItem/{check_item_id}"
    headers = {"Accept": "application/json"}
    state_str = "complete" if is_complete else "incomplete"
    query = {
        'state': state_str,
        **KEY_TOKEN
    }
    response = await client.put(url, headers=headers, params=query)
    try:
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPStatusError, json.JSONDecodeError) as e:
        print(f"Error updating check item state: {e}")
        return response.text