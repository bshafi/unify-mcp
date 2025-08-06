from agents import Agent, Runner, add_trace_processor, TracingProcessor, Trace
from agents.mcp.server import MCPServerStdio
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
import dotenv
dotenv.load_dotenv()

import os

model_name = os.environ['OPENAI_MAIN_MODEL']

from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from agents.exceptions import InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio


async def main(message):
    "Uses the MCP Server to manage cards for all tasks in Trello"

    async with MCPServerStdio(
        params={
            "command": "python",
            "args": ["mcp_server.py"],
        }
    ) as server:

        trello_agent = Agent(
            model=model_name,
            name="Trello Agent",
            instructions=prompt_with_handoff_instructions(
                "The following text is part of a conversation between coworkers."
                "IF there are any mention of a task, verify the structure of the Trello board and update it accordingly."
                "IF a person is mentioned use the assignment_agent to assign the task on the Trello board."
                "IF a person is taken off of a job, verify the structure of the card and remove that person from the job. Only remove one person at a time."
                "IF you can't find a task on the board create it before updating."
                "Do nothing else if the text is not relevant or if an operation fails in any way."
            ),
            mcp_servers=[
                server
            ]
            # output_type=bool # Returns a whether a task was assigned
        )

        query = message.content
        try:
            result = await Runner.run(trello_agent, query)
            print('QUERY:', query)
            print('AGENT:', result.final_output)
        except InputGuardrailTripwireTriggered as e:
            print("Guardrail blocked this input:", e)

if __name__ == "__main__":
    import discord_background
    
    discord_background.run_discord_bot(main)
