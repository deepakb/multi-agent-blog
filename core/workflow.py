import functools
from langgraph.graph import StateGraph, END


from core.supervisor_chain import get_supervisor_chain
from agents.lotto_agent import get_lotto_agent
from agents.math_agent import get_math_agent
from agents.agent_node import agent_node
from core.agent_state import AgentState


def build_workflow(llm, config, members):
    supervisor_chain = get_supervisor_chain(llm, members, ["FINISH"] + members)
    workflow = StateGraph(AgentState)
    lotto_agent = get_lotto_agent(llm)
    math_agent = get_math_agent(llm)

    workflow.add_node("Lotto_Manager", functools.partial(
        agent_node, agent=lotto_agent, name="Lotto_Manager"))
    workflow.add_node("Math_Agent", functools.partial(
        agent_node, agent=math_agent, name="Math_Agent"))
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
