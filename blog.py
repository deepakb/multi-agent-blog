from langchain_openai import ChatOpenAI
from typing import Annotated, List, Tuple, Union
from langchain.tools import BaseTool, StructuredTool, Tool
from langchain_experimental.tools import PythonREPLTool
from langchain_core.tools import tool
import random
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import operator
from typing import Annotated, Any, Dict, List, Optional, Sequence, TypedDict
import functools

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END


llm = ChatOpenAI(model="gpt-3.5-turbo")

# This executes code locally, which can be unsafe
python_repl_tool = PythonREPLTool()


@tool("sum_numbers", return_direct=False)
def sum_numbers(input: str) -> str:
    """Returns the sum of the given numbers input."""
    print(input)
    return 10, 2, 3, 4, 5, 6, 6, 8, 9, 14


@tool("lower_case", return_direct=False)
def to_lower_case(input: str) -> str:
    """Returns the input as all lower case."""
    return input.lower()


@tool("random_number", return_direct=False)
def random_number_maker(input: str) -> str:
    """Returns a random number between 0-100. input the word 'random'"""
    return random.randint(0, 100)


tools = [to_lower_case, random_number_maker, sum_numbers]


def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    # Each worker node will be given a name and some tools.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor


def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}


members = ["Lotto_Manager", "Math_Agent"]
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers:  {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)
# Our team supervisor is an LLM node. It just picks the next agent to process
# and decides when the work is completed
options = ["FINISH"] + members
# Using openai function calling can make output parsing easier for us
function_def = {
    "name": "route",
    "description": "Select the next role.",
    "parameters": {
        "title": "routeSchema",
        "type": "object",
        "properties": {
            "next": {
                "title": "Next",
                "anyOf": [
                    {"enum": options},
                ],
            }
        },
        "required": ["next"],
    },
}
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next?"
            " Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join(members))


supervisor_chain = (
    prompt
    | llm.bind_functions(functions=[function_def], function_call="route")
    | JsonOutputFunctionsParser()
)

# The agent state is the input to each node in the graph


class AgentState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The 'next' field indicates where to route to next
    next: str


lotto_agent = create_agent(
    llm, tools, "You are a senior lotto manager. you run the lotto and get random numbers")
lotto_node = functools.partial(
    agent_node, agent=lotto_agent, name="Lotto_Manager")

# NOTE: THIS PERFORMS ARBITRARY CODE EXECUTION. PROCEED WITH CAUTION
math_agent = create_agent(
    llm, [sum_numbers], "You are a math majesto who can sum the given numbers")
math_node = functools.partial(
    agent_node, agent=math_agent, name="Math_Agent")

workflow = StateGraph(AgentState)
workflow.add_node("Lotto_Manager", lotto_node)
workflow.add_node("Math_Agent", math_node)
workflow.add_node("supervisor", supervisor_chain)

for member in members:
    # We want our workers to ALWAYS "report back" to the supervisor when done
    # add one edge for each of the agents
    workflow.add_edge(member, "supervisor")

# The supervisor populates the "next" field in the graph state
# which routes to a node or finishes
conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END
workflow.add_conditional_edges(
    "supervisor", lambda x: x["next"], conditional_map)
# Finally, add entrypoint
workflow.set_entry_point("supervisor")

graph = workflow.compile()

config = {"recursion_limit": 20}
for s in graph.stream(
    {
        "messages": [
            HumanMessage(
                content="Get 10 random lotto numbers and give the sum of those number along with 10 numbers.")
        ]
    }, config=config
):
    if "__end__" not in s:
        print(s)
        print("----")
