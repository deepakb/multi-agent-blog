

import functools
from langgraph.graph import StateGraph, END

from core.supervisor_chain import get_supervisor_chain
from agents.research_agent import get_research_agent
from agents.outliner_agent import get_outliner_agent
from agents.content_writer_agent import get_content_writer_agent
from agents.seo_agent import get_seo_agent
from agents.editor_agent import get_editor_agent
from agents.agent_node import agent_node
from core.agent_state import AgentState


def build_workflow(llm, config, members):
    supervisor_chain = get_supervisor_chain(llm, members, ["FINISH"] + members)
    workflow = StateGraph(AgentState)

    # Create agents
    research_agent = get_research_agent(llm)
    outliner_agent = get_outliner_agent(llm)
    content_writer_agent = get_content_writer_agent(llm)
    seo_agent = get_seo_agent(llm)
    editor_agent = get_editor_agent(llm)

    # Add nodes to workflow
    workflow.add_node("Research_Agent", functools.partial(
        agent_node, agent=research_agent, name="Research_Agent"))
    workflow.add_node("Outliner_Agent", functools.partial(
        agent_node, agent=outliner_agent, name="Outliner_Agent"))
    workflow.add_node("Content_Writer_Agent", functools.partial(
        agent_node, agent=content_writer_agent, name="Content_Writer_Agent"))
    workflow.add_node("SEO_Agent", functools.partial(
        agent_node, agent=seo_agent, name="SEO_Agent"))
    workflow.add_node("Editor_Agent", functools.partial(
        agent_node, agent=editor_agent, name="Editor_Agent"))
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
