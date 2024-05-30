import functools
from langgraph.graph import StateGraph, END

from core.supervisor_chain import get_supervisor_chain
from agents.topic_agent import get_topic_agent
from agents.agent_node import agent_node
from core.agent_state import AgentState


def build_workflow(llm, members):
    supervisor_chain = get_supervisor_chain(llm, members, ["FINISH"] + members)
    workflow = StateGraph(AgentState)

    # Create agents
    topic_agent = get_topic_agent(llm)

    # Add nodes to workflow
    workflow.add_node("Topic_Agent", functools.partial(
        agent_node, agent=topic_agent, name="Topic_Agent"))
    workflow.add_node("supervisor", supervisor_chain)

    for member in members:
        workflow.add_edge(member, "supervisor")

    conditional_map = {k: k for k in members}
    conditional_map["FINISH"] = END
    workflow.add_conditional_edges(
        "supervisor", lambda x: x["next"], conditional_map
    )
    workflow.set_entry_point("supervisor")

    return workflow.compile()
