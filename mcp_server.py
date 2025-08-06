from fastmcp import FastMCP
from typing import Optional

import trello_api

mcp = FastMCP("Unify-MCP")


@mcp.tool
async def create_card(name: str, description: str):
    """
    Whenever a person is asked to do a task a card is created with
    a name for the task and a description of what the task entails.

    Create card with the provided `name` and description
    """

    lists = trello_api.get_lists(trello_api.BOARD_ID)
    list_id = lists[0]["id"]

    trello_api.create_card_in_list(list_id, name, description)


@mcp.tool
async def move_card(card_name: str, new_list_name: str):
    """
    Whenever a task is updated, the card is moved to a different list.
    Moves a Trello card with the given `card_name` to the `new_list_name`.
    """
    cards = trello_api.get_cards(trello_api.BOARD_ID)
    card_to_move = next((c for c in cards if c["name"] == card_name), None)
    if not card_to_move:
        return f"Card '{card_name}' not found."

    lists = trello_api.get_lists(trello_api.BOARD_ID)
    target_list = next((l for l in lists if l["name"] == new_list_name), None)
    if not target_list:
        return f"List '{new_list_name}' not found."

    return trello_api.update_card_list(card_to_move["id"], target_list["id"])

@mcp.tool
async def get_trello_structure() -> str:
    """
    Returns the current structure of the Trello board.
    """
    lists = trello_api.get_lists(trello_api.BOARD_ID)
    cards = trello_api.get_cards(trello_api.BOARD_ID)

    structure = "Trello Board Structure:\n"
    for lst in lists:
        structure += f"List: {lst['name']}\n"
        for card in cards:
            if card["idList"] == lst["id"]:
                structure += f"  - Card: {card['name']}\n"
    return structure


if __name__ == "__main__":
    mcp.run()
