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
async def get_board_structure() -> str:
    """
    Returns all lists and cards in the Trello board.
    """
    lists = await trello_api.get_lists(trello_api.BOARD_ID)
    cards = await trello_api.get_cards(trello_api.BOARD_ID)

    structure = "Trello Board Structure:\n"
    for lst in lists:
        structure += f"Cards in list \"{lst['name']}\":\n"
        for card in cards:
            if card["idList"] == lst["id"]:
                structure += f"- {card['name']}\n"
    return structure


if __name__ == "__main__":
    mcp.run()
