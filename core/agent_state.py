from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: BaseMessage
    # The 'next' field indicates where to route to next
    next: str
