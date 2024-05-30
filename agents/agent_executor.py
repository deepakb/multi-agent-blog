from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.output_parsers import PydanticOutputParser


def create_agent(
    llm: ChatOpenAI,
    tools: list,
    system_prompt: str,
    parser: PydanticOutputParser
) -> AgentExecutor:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    ).partial(
        format_instructions=parser.get_format_instructions(),
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor
