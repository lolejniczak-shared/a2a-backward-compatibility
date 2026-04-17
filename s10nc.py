from executor import (
    HelloWorldAgentExecutor,  # type: ignore[import-untyped]
)

from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill, AgentInterface



skill = AgentSkill(
        id='hello_world',
        name='Returns hello world',
        description='just returns hello world',
        tags=['hello world'],
        examples=['hi', 'hello world'],
    )


##https://a2a-protocol.org/latest/specification/#441-agentcard
agent_card = AgentCard(
        name='Hello World Agent',
        description='Just a hello world agent',
        supported_interfaces = [
            AgentInterface(
                url = "http://localhost:9999/", protocol_binding = "JSONRPC", protocol_version = "1.0" ##, tenant = "default"
            )
        ],
        default_input_modes=['text/plain'], ##must be valid media type
        default_output_modes=['text/plain'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
        version = "0.0.1" ## this is version of agent, not of the protocol. Protocol version is availble through supported interfaces
    )

request_handler = DefaultRequestHandler(
        agent_executor=HelloWorldAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

server = A2AFastAPIApplication(
        agent_card=agent_card, http_handler=request_handler
    )

import uvicorn

print("A2A server v 1.0 without compatibility with 0.3")
uvicorn.run(server.build(), host='0.0.0.0', port=9999)