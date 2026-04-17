import httpx
from uuid import uuid4
import asyncio
from typing import Any
from google.protobuf.struct_pb2 import Struct, Value
from contextlib import aclosing
from a2a.types import SendMessageRequest, Message, Part, Role
from a2a.client import A2ACardResolver
from a2a.client.client_factory import ClientFactory, ClientConfig
from contextlib import aclosing
import json

AGENT_URL = 'http://localhost:9999'
USER_QUERY = 'What will be the role of agentic protocols in agentic economy?'

async def main():
    async with httpx.AsyncClient(
            headers={
                ##"Authorization": f"Bearer {BEARER_TOKEN}",
                "Content-Type": "application/json",
            }
    ) as httpx_client:
        resolver = A2ACardResolver(httpx_client, AGENT_URL)
        card = await resolver.get_agent_card()
        print('\n✓ Agent Card Found:')
        print(f'  Name: {card.name}')

        config = ClientConfig(httpx_client=httpx_client)

        client = await ClientFactory(config).create_from_url(
            url=AGENT_URL,
        )

        msg = Message(
            role=Role.ROLE_USER, ##instead of user
            message_id=f'stream-{uuid4()}',
            parts=[
                Part(text=USER_QUERY), ##'kind': 'text', there is no kind field in 1.0

            ]
        )

        async for event in client.send_message(request=SendMessageRequest(message=msg)):
            print(f"Agent says: {event}")


if __name__ == '__main__':
    asyncio.run(main())