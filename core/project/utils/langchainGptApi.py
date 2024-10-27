import logging
import os.path

from langchain_community.callbacks import get_openai_callback
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

log = logging.getLogger(__name__)

"""For later CSV file support"""
# from langchain_community.document_loaders.csv_loader import CSVLoader
# from langchain.agents import create_csv_agent
# from langchain.embeddings import OpenAIEmbeddings


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


def getResponseFromApi(question):
    response_data = {}
    input_data = [HumanMessage(question)]

    with get_openai_callback() as callable:
        result = app.invoke({"messages": input_data}, config)

        response_data = {
            "response_text": result["messages"][-1].content,
            "completion_tokens": callable.completion_tokens,
            "prompt_tokens": callable.prompt_tokens,
            "total_price": callable.total_cost,
        }

    return response_data
