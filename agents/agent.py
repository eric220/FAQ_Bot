from typing import Annotated, Literal, Union, Optional, Dict
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages.ai import AIMessage
from config_files import config
from db import chroma_db
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, InjectedState
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.runnables import RunnableConfig
from langchain_core.messages.tool import ToolMessage
from langgraph.types import Command
import uuid
import time
from langgraph.checkpoint.memory import MemorySaver
from agents.tools import query_tool
memory = MemorySaver()

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


class Agent:
    def __init__(self):
        model_name = 'gpt-4o-mini'
        llm = ChatOpenAI(model_name = model_name, openai_api_key = config.OPENAI_API_KEY)
        tools = [query_tool.get_results]
        tool_node = ToolNode(tools)
        self.llm_with_tools = llm.bind_tools(tools)
        graph_builder = StateGraph(AgentState)
        graph_builder.add_node("chatbot", self.chatbot)
        graph_builder.set_entry_point("chatbot")
        graph_builder.add_node("tools", tool_node)
        graph_builder.add_conditional_edges("chatbot", self.conditional_route_to_tools)
        graph_builder.add_edge('tools', 'chatbot')
        self.graph = graph_builder.compile(checkpointer=memory)

    JIMMY_BOT_INST = (
        "system",
        '''You are a helpful question answering bot. always use the get_results tool to search for the most
        likely answers. always answer in the first person. For example if the user asks your age, respond I am 21 years old.'''
    
        '''always use the get_results tool. if the answers returned don't seem relevant, inform the user that you will
        notify the correct person''')

    def conditional_route_to_tools(self, state: AgentState):
        """Route between chatbot and tool tool nodes, depending if a tool call is made."""
        if not (msgs := state.get("messages", [])):
            raise ValueError(f"No messages found when parsing state: {state}")
        msg = msgs[-1]
        if hasattr(msg, "tool_calls") and len(msg.tool_calls) > 0:
            return "tools"
        return END

    def chatbot(self, state: AgentState):
        if state["messages"]:
            new_output = self.llm_with_tools.invoke([self.JIMMY_BOT_INST] + state["messages"])
        else:
            new_output = AIMessage(content='')
        
        return {"messages": new_output}


    def get_response(self, query, config_id):
        config = {"configurable": {"thread_id": config_id}}
        return self.graph.invoke({'messages': query}, config=config )#['messages'][-1].content
    