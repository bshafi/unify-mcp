from agents import Agent, Runner
from agents.mcp.server import MCPServerStdio

import dotenv
dotenv.load_dotenv()

import os

model_name = os.environ['OPENAI_MAIN_MODEL']

from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from agents.exceptions import InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio


async def main():
    "Uses the MCP Server to create cards in trello"
    async with MCPServerStdio(
        params={
            "command": "python",
            "args": ["mcp_server.py"],
        }
    ) as server:

        trello_agent = Agent(
            model=model_name,
            name="Trello Agent",
            instructions="If a task was assigned use MCP and create a trello card with a name for the task and a description. The following text is part of a conversation between coworkers. ",
            mcp_servers=[
                server
            ],
            output_type=bool # Returns a whether a task was assigned
        )
        try:
            result = await Runner.run(trello_agent, "John, make copies of the report and put it on my desk.")
            print(result.final_output)
        except InputGuardrailTripwireTriggered as e:
            print("Guardrail blocked this input:", e)
        try:
            result = await Runner.run(trello_agent, "John, how was your day.")
            print(result.final_output)
        except InputGuardrailTripwireTriggered as e:
            print("Guardrail blocked this input:", e)

if __name__ == "__main__":
    asyncio.run(main())