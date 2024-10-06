import os.path

from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI

"""For later CSV file support"""
# from langchain_community.document_loaders.csv_loader import CSVLoader
# from langchain.agents import create_csv_agent
# from langchain.embeddings import OpenAIEmbeddings


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    model="gpt-4o-mini",
    stream_usage=True,
)


def getResponseFromApi(question):
    response_data = {}

    with get_openai_callback() as callable:
        result = llm.invoke(question)

        response_data = {
            "response_text": result.content,
            "completion_tokens": callable.completion_tokens,
            "prompt_tokens": callable.prompt_tokens,
            "total_price": callable.total_cost,
        }

    return response_data
