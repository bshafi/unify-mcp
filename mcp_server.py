from fastmcp import FastMCP
from typing import Optional

import trello_api

mcp = FastMCP("Unify-MCP")


@mcp.tool
async def create_card(list_name: str, card_name: str, description: str):
    """
    Create card for a task in the specified list with a description of what the task entails.
    """
    lists = await trello_api.get_lists(trello_api.BOARD_ID)
    target_list = next((l for l in lists if l["name"] == list_name), None)
    if not target_list:
        return f"List '{list_name}' not found."

    return await trello_api.create_card_in_list(
        target_list["id"], card_name, description
    )


@mcp.tool
async def move_card(card_name: str, new_list_name: str):
    """
    Whenever a task is updated, the card is moved to a different list.
    Moves a Trello card with the given `card_name` to the `new_list_name`.
    """
    cards = await trello_api.get_cards(trello_api.BOARD_ID)
    card_to_move = next((c for c in cards if c["name"] == card_name), None)
    if not card_to_move:
        return f"Card '{card_name}' not found."

    lists = await trello_api.get_lists(trello_api.BOARD_ID)
    target_list = next((l for l in lists if l["name"] == new_list_name), None)
    if not target_list:
        return f"List '{new_list_name}' not found."

    return await trello_api.update_card_list(card_to_move["id"], target_list["id"])


@mcp.tool
async def get_trello_structure() -> str:
    """
    Returns the current structure of the Trello board.
    """
    lists = await trello_api.get_lists(trello_api.BOARD_ID)
    cards = await trello_api.get_cards(trello_api.BOARD_ID)

    structure = "Trello Board Structure:\n"
    for lst in lists:
        structure += f"List: {lst['name']}\n"
        for card in cards:
            if card["idList"] == lst["id"]:
                structure += f"  - Card: {card['name']}\n"
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
