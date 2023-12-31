from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import pandas as pd
import langchain
import re

df=pd.read_csv("data.csv")

def run_query_save_results():
    res = [list(df[column].unique()) for column in df.columns if column in ["Stage","HUB","REV Opportunity Source"]]
    res = [str(el) for sub in res for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return res

texts=run_query_save_results()

embeddings = langchain.embeddings.openai.OpenAIEmbeddings()
vector_db = Chroma.from_texts(texts, embeddings)
retriever = vector_db.as_retriever()

retriever_tool = create_retriever_tool(
    retriever,
    name="name_search",
    description="use to learn how a piece of data is actually written, can be from Hubs etc",
)

custom_tool_list = [retriever_tool]
