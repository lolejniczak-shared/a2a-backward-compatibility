from executor import (
    HelloWorldAgentExecutor,  
)

from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill, AgentInterface
from a2a.server.routes import (
    create_agent_card_routes,
    create_jsonrpc_routes,
    create_rest_routes,
)
from fastapi import FastAPI
import uvicorn

host = "0.0.0.0"
port = 9999

# 1. Define Skills and Agent Card
skill = AgentSkill(
    id='hello_world',
    name='Returns hello world',
    description='just returns hello world',
    tags=['hello world'],
    examples=['hi', 'hello world'],
)

agent_card = AgentCard(
    name='Hello World Agent',
    description='Just a hello world agent',
    supported_interfaces=[
        AgentInterface(
            url=f'http://{host}:{port}/a2a/jsonrpc',
            protocol_binding="JSONRPC", 
            protocol_version="1.0"
        ),
        AgentInterface(
            url=f'http://{host}:{port}/a2a/jsonrpc',
            protocol_binding="JSONRPC", 
            protocol_version="0.3"
        )
    ],
    default_input_modes=['text/plain'],
    default_output_modes=['text/plain'],
    capabilities=AgentCapabilities(streaming=True),
    skills=[skill],
    version="0.0.1"
)

# 2. Setup Handlers
request_handler = DefaultRequestHandler(
    agent_card=agent_card,
    agent_executor=HelloWorldAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

# 3. Create Routes
rest_routes = create_rest_routes(
    request_handler=request_handler,
    path_prefix='/a2a/rest',
    enable_v0_3_compat=True,
)

jsonrpc_routes = create_jsonrpc_routes(
    request_handler=request_handler,
    rpc_url='/a2a/jsonrpc',
    enable_v0_3_compat=True,
)

agent_card_routes = create_agent_card_routes(
    agent_card=agent_card,
)

# 4. Initialize FastAPI and mount routes
app = FastAPI()

app.routes.extend(agent_card_routes)
app.routes.extend(jsonrpc_routes)
app.routes.extend(rest_routes)

# 5. Execution Logic
if __name__ == "__main__":
    print(f"A2A server v 1.0 with compatibility  starting on port {port}...")
    uvicorn.run("s10c03new:app", host=host, port=port, reload=True)
