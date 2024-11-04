import logging
import os.path

import pandas as pd
from langchain.agents import AgentExecutor
from langchain_community.callbacks import get_openai_callback
from langchain_core.messages import HumanMessage
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

log = logging.getLogger(__name__)

if not os.getenv("OPENAI_API_KEY"):
    log.error("NO API KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    stream_usage=True,
)

workflow = StateGraph(MessagesState)


# Callback function for persistence
def __call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": response}


workflow.add_edge(START, "llm")
workflow.add_node("llm", __call_model)

# Memory for checkpointing the llm context
memory = MemorySaver()
app = workflow.compile(memory)

# Thread configuration
config = {"configurable": {"thread_id": "1"}}

# File related configuration of the Agent
dfAgent: AgentExecutor = None

# Altering the final LLM in case a file is sent
request_llm = None


def getResponseFromApi(question: str, file_path: str = None):
    global dfAgent
    global request_llm
    response_data = {}
    input_data = [HumanMessage(question)]

    # No need to use the DataFrame agent if the user only sends
    # normal messages
    if not request_llm:
        request_llm = app

    # Files should always be CSV or XLSX
    if file_path:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise TypeError("Wrong File type")

        dfAgent = create_pandas_dataframe_agent(
            llm,
            df,
            agent_type="openai-tools",
            allow_dangerous_code=True,  # Later to be implemented a Docker Container
        )
        # Redefines the final LLM as a DataFrame Agent, this raises
        # a problem of the context window about the previous file sent, that means
        # it would lose context of any older file sent, in case of sending a new File;
        # A simple conditional logic would fix this
        request_llm = dfAgent

    with get_openai_callback() as callable:
        # Agents keep the context of the coversation, so the question is passed directly
        result = request_llm.invoke(
            {"input": question} if dfAgent else {"messages": input_data}, config
        )

        response_data = {
            "response_text": result["output"]
            if dfAgent
            else result["messages"][-1].content,
            "completion_tokens": callable.completion_tokens,
            "prompt_tokens": callable.prompt_tokens,
            "total_price": callable.total_cost,
        }

    return response_data
