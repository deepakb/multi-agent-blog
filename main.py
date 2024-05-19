from langchain_openai import ChatOpenAI
from core.workflow import build_workflow
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-3.5-turbo")
members = ["Lotto_Manager", "Math_Agent"]

graph = build_workflow(llm, {"recursion_limit": 20}, members)

for s in graph.stream(
    {
        "messages": [
            HumanMessage(
                content="Get 10 random lotto numbers and give the sum of those number along with 10 numbers.")
        ]
    }, config={"recursion_limit": 20}
):
    if "__end__" not in s:
        print(s)
        print("----")
