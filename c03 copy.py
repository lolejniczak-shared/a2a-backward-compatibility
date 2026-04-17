import httpx
from uuid import uuid4
import asyncio
from typing import Any

from a2a.client.middleware import ClientCallInterceptor 
from a2a.client.client_factory import ClientFactory, ClientConfig

from google import auth as google_auth
from google.auth.transport import requests as google_requests
import uuid
import requests
from google.oauth2 import id_token
from a2a.client import A2ACardResolver
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

        client = await ClientFactory.connect(
            agent=card, 
            client_config=config,
            relative_card_path='/.well-known/agent-card.json'
        )

        message_payload = {
            'role': 'user',
            'parts': [{'kind': 'text', 'text': USER_QUERY}],
            'messageId': uuid4().hex,
            'contextId': '959304c1-e814-4486-b9a7-efe885a6b066'
        }

        # Send raw dictionary
        resp = client.send_message(message_payload)
        
        final_response = None
        async for response_chunk in resp:
            if isinstance(response_chunk, tuple):
                final_response = response_chunk[0]
            else:
                final_response = response_chunk
        
        if final_response:
            print("--- Final Response ---")
            print(final_response.model_dump(mode='json', exclude_none=True))

if __name__ == '__main__':
    asyncio.run(main())