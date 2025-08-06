from fastmcp import FastMCP
from typing import Optional, List

import trello_api

mcp = FastMCP("Unify-MCP")


@mcp.tool
async def create_card(list_name: str, card_name: str, description: str):
    """
    Creates a card in the a list with a description.
    """
    lists = await trello_api.get_lists(trello_api.BOARD_ID)
    target_list = next((l for l in lists if l["name"] == list_name), None)
    if not target_list:
        return f"List '{list_name}' not found."

    result = await trello_api.create_card_in_list(
        target_list["id"], card_name, description
    )

    if isinstance(result, dict):
        return "card_created"

    return result


@mcp.tool
async def move_card(card_name: str, list_name: str):
    """
    Moves a card to another list.
    """
    cards = await trello_api.get_cards(trello_api.BOARD_ID)
    card_to_move = next((c for c in cards if c["name"] == card_name), None)
    if not card_to_move:
        return f"Card '{card_name}' not found."

    lists = await trello_api.get_lists(trello_api.BOARD_ID)
    target_list = next((l for l in lists if l["name"] == list_name), None)
    if not target_list:
        return f"List '{list_name}' not found."

    result = await trello_api.update_card_list(card_to_move["id"], target_list["id"])

    if isinstance(result, dict):
        return "card_moved"

    return f"Failed to move card '{card_name}' to list '{list_name}'."


@mcp.tool
async def manage_checklist(card_name: str, checklist_name: str, items: List[str]):
    """
    Adds a checklist to a card.
    If the checklist already exists, it adds the specified items to it.
    If it doesn't exist, it creates the checklist first and then adds the items.
    """
    cards = await trello_api.get_cards(trello_api.BOARD_ID)
    target_card = next((c for c in cards if c["name"] == card_name), None)
    if not target_card:
        return f"Card '{card_name}' not found."

    card_id = target_card['id']
    checklists = await trello_api.get_checklists_on_card(card_id)
    target_checklist = next((cl for cl in checklists if cl['name'] == checklist_name), None)

    if not target_checklist:
        target_checklist = await trello_api.create_checklist(card_id, checklist_name)
        if not isinstance(target_checklist, dict):
            return f"Failed to create checklist '{checklist_name}': {target_checklist}"
    
    checklist_id = target_checklist['id']

    for item_name in items:
        result = await trello_api.create_check_item(checklist_id, item_name)
        if not isinstance(result, dict):
            return f"Failed to add item '{item_name}' to checklist '{checklist_name}'."
    
    return "checklist_updated"


@mcp.tool
async def complete_checklist_item(card_name: str, item_name: str, completed: bool = True):
    """
    Marks a task in a checklist as complete or incomplete.
    """
    cards = await trello_api.get_cards(trello_api.BOARD_ID)
    target_card = next((c for c in cards if c["name"] == card_name), None)
    if not target_card:
        return f"Card '{card_name}' not found."
    card_id = target_card['id']

    checklists = await trello_api.get_checklists_on_card(card_id)
    if not checklists:
        return f"No checklists found on card '{card_name}'."
    
    target_item = None
    for cl in checklists:
        # checkItems key should exist because we requested it in the API call
        for item in cl.get('checkItems', []):
            if item['name'] == item_name:
                target_item = item
                break
        if target_item:
            break
    
    if not target_item:
        return f"Checklist item '{item_name}' not found on card '{card_name}'."
    
    result = await trello_api.update_check_item_state(card_id, target_item['id'], completed)

    if isinstance(result, dict):
        return "checklist_item_updated"
    
    return f"Failed to update item '{item_name}': {result}"

@mcp.tool
async def set_card_description(card_name: str, description: str):
    """
    Sets or updates the description for an existing card.
    """
    cards = await trello_api.get_cards(trello_api.BOARD_ID)
    card_to_update = next((c for c in cards if c["name"] == card_name), None)
    if not card_to_update:
        return f"Card '{card_name}' not found."

    result = await trello_api.update_card_description(card_to_update["id"], description)
    
    if isinstance(result, dict):
        return "card_description_updated"

    return f"Failed to update description for card '{card_name}'."

@mcp.tool
async def get_board_contents() -> str:
    """
    Returns all Lists and Cards/Tasks in the Trello board.
    """
    lists = await trello_api.get_lists(trello_api.BOARD_ID)
    cards = await trello_api.get_cards(trello_api.BOARD_ID)

    structure = "Trello Board Structure:\n"
    for lst in lists:
        structure += f"Cards in list \"{lst['name']}\":\n"
        for card in cards:
            if card["idList"] == lst["id"]:
                structure += f"- {card['name']}\n"
                for checklist in await trello_api.get_checklists_on_card(card["id"]):
                    structure += f"  - Checklist: {checklist['name']}\n"
                    for item in checklist.get('checkItems', []):
                        status = "✅" if item['state'] == 'complete' else "❌"
                        structure += f"    - {status} {item['name']}\n"
    return structure

@mcp.tool
async def asign_card(card_name: str, person_name: str):
    """
    Updates a trello card and assigns a specific person to the card
    `card_name` is the name of the card
    `person_name` is the name of the person
    """
    
    cards = await trello_api.get_cards(trello_api.BOARD_ID)
    card_id = next((c for c in cards if c["name"] == card_name), None)['id']
    if not card_id:
        return f"Card '{card_name}' not found."
    members = await trello_api.get_members(trello_api.BOARD_ID)

    member_id = next((c for c in members if person_name.lower() in c["fullName"].lower() or person_name.lower() in c['username']), None)
    member_id = member_id['id']
    if not member_id:
        return f"Card '{person_name}' not found."

    return await trello_api.assign_card(card_id, member_id)

@mcp.tool
async def remove_person_from_card(card_name: str, person_name: str):
    """
    Removes a person assigned to a specific card.
    
    """
    cards = await trello_api.get_cards(trello_api.BOARD_ID)
    card_id = next((c for c in cards if c["name"] == card_name), None)['id']
    if not card_id:
        return f"Card '{card_name}' not found."
    members = await trello_api.get_members(trello_api.BOARD_ID)

    member_id = next((c for c in members if person_name.lower() in c["fullName"].lower() or person_name.lower() in c['username']), None)
    member_id = member_id['id']
    if not member_id:
        return f"Card '{person_name}' not found."

    return await trello_api.remove_card_assignment(card_id, member_id)

@mcp.tool
async def get_card_structure(card_name: str):
    """
    Retrives details about a card. Use this whenever you're modifying a card
    """
    cards = await trello_api.get_cards(trello_api.BOARD_ID)
    card_id = next((c for c in cards if c["name"] == card_name), None)['id']
    if not card_id:
        return f"Card '{card_name}' not found."
    
    return await trello_api.get_card_members(card_id)

if __name__ == "__main__":
    mcp.run()