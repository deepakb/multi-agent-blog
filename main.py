from langchain_openai import ChatOpenAI

from core.workflow import build_workflow
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-3.5-turbo")
members = [
    "Research_Agent",
    "Outliner_Agent",
    "Content_Writer_Agent",
    "SEO_Agent",
    "Editor_Agent"
]

graph = build_workflow(llm, {"recursion_limit": 20}, members)

for s in graph.stream(
    {
        "messages": [
            HumanMessage(
                content="Create a blog post on the topic 'The Future of AI in Healthcare'."
            )
        ]
    }, config={"recursion_limit": 20}
):
    if "__end__" not in s:
        print(s)
        print("----")
