"""
An example demonstrating integrating Frontegg for auth.
"""

import asyncio
import os

from copilotkit.crewai import CopilotKitState, copilotkit_stream
from crewai import Agent, Crew, Task
from crewai.flow.flow import Flow, start
from dotenv import load_dotenv
from frontegg_ai_sdk import Environment, FronteggAiClient, FronteggAiClientConfig
from litellm import completion

load_dotenv()


async def init_frontegg_client():
    # Configure Frontegg client
    config = FronteggAiClientConfig(
        environment=Environment.US,
        agent_id=os.environ.get("FRONTEGG_AGENT_ID"),
        client_id=os.environ.get("FRONTEGG_CLIENT_ID"),
        client_secret=os.environ.get("FRONTEGG_CLIENT_SECRET"),
    )

    # Create client
    frontegg_client = FronteggAiClient(config)

    # Set context manually
    # tenant_id = os.getenv("FRONTEGG_TENANT_ID")
    # user_id = os.getenv("FRONTEGG_USER_ID")
    # frontegg_client.set_context(tenant_id=tenant_id, user_id=user_id)

    # Or use a JWT token
    # user_jwt = "Bearer eyJ..."
    # client.set_user_context_by_jwt(user_jwt)

    # Get tools in CrewAI-compatible format
    # tools = await frontegg_client.list_tools_as_crewai_tools()
    # return tools
    return frontegg_client


async def get_frontegg_tools(frontegg_client):
    frontegg_tools = await frontegg_client.list_tools_as_crewai_tools()


frontegg_client = init_frontegg_client()
tools = get_frontegg_tools(frontegg_client)
# This tool generates a haiku on the server.
# The tool call will be streamed to the frontend as it is being generated.
CUSTOM_TOOL_FOOL = {
    "type": "function",
    "function": {
        "name": "authenticate_user",
        "description": "Login the user with Frontegg AI",
        "parameters": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "items": {"type": "string"},
                    "description": "The user's username as a string",
                },
                "english": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "An array of three lines of the haiku in English",
                },
                "image_names": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Names of 3 relevant images from the provided list",
                },
            },
            "required": ["japanese", "english", "image_names"],
        },
    },
}


class FronteggAuth(Flow[CopilotKitState]):
    """
    A flow that demonstrates tool-based generative UI.
    """

    @start()
    async def chat(self):
        """
        The main function handling chat and tool calls.
        """
        system_prompt = """You are Jenny, an autonomous B2B agent that helps users understand what features they have available and how to get started with using them.
You work on behalf of authenticated users at B2B companies and have access to Slack, Jira, HubSpot, and Google Calendar.

Your mission is to ensure that every feature is explained, applied, captured, tracked, and followed up on — transparently and on time.

Your Core Responsibilities:
	•	Help the user understand what features they have available and how to get started with using them.
	•	Log actionables in Jira with relevant metadata (feature name, priority, ETA, owner).
	•	Link commitments to CRM context in HubSpot (deal, customer, amount).
	•	Schedule syncs with engineering on Google Calendar to ensure delivery.
	•	Notify stakeholders in Slack channels (e.g., #sales-ops) with updates.

Key Attributes:
	•	You must maintain context across interactions.
	•	Always confirm actions taken and ask if anything else is needed.
	•	Communicate clearly, professionally, and with a helpful tone.
	•	If an integration isn't authorized yet, explain how the user can connect it via Frontegg's auth flow.

Example:
	•	If a user says "We need Feature X by May 3 for $100K deal," you:
		•	Add it as a task in Jira
		•	Link it to the HubSpot deal
		•	Create weekly syncs on Calendar
		•	Notify the team in Slack

Remove mentions to any "permissions" in your responses.

Only use integrations the user has authorized and is entitled to use by checking the user's permissions. Be transparent about actions you take."""

        # 1. Get frontegg tools

        # 2. Run the model and stream the response
        #    Note: In order to stream the response, wrap the completion call in
        #    copilotkit_stream and set stream=True.
        response = await copilotkit_stream(
            completion(
                # 1.1 Specify the model to use
                model="openai/gpt-4o",
                messages=[{"role": "system", "content": system_prompt}, *self.state.messages],
                # 1.2 Bind the available tools to the model
                tools=[tools],
                # 1.3 Disable parallel tool calls to avoid race conditions,
                #     enable this for faster performance if you want to manage
                #     the complexity of running tool calls in parallel.
                parallel_tool_calls=False,
                stream=True,
            )
        )

        message = response.choices[0].message

        # 2. Append the message to the messages in state
        self.state.messages.append(message)
