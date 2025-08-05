from fastmcp import FastMCP
from typing import Optional

import trello_api

mcp = FastMCP('Unify-MCP')
@mcp.tool
async def create_card(name: str, description: str):
    """
        Whenever a person is asked to do a task a card is created with 
        a name for the task and a description of what the task entails.

        Create card with the provided `name` and description
    """

    lists = trello_api.get_lists(trello_api.BOARD_ID)
    list_id = lists[0]['id']


    trello_api.create_card_in_list(list_id, name, description)




if __name__ == "__main__":
    mcp.run()