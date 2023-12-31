from langchain.chat_models import AzureChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import io
from PIL import Image
from open_ai_objects import llm_dict
from retriever import custom_tool_list


def create_agent(filename: str,llm_name:str,custom_suffix:str, custom_prefix:str):
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        filename: The path to the CSV file that contains the data.

    Returns:
        An agent that can access and use the LLM.
    """


    # custom_suffix = """
    # If a user asks for me to filter based on proper nouns, I should first check the spelling using the name_search tool.
    # Otherwise, I can then look at the dataframe to see what I can query.
    # """

    # Read the CSV file into a Pandas DataFrame.
    df = pd.read_csv(filename)
    df.loc[:,["HUB"]] = df.HUB.str.strip()

    agent =create_pandas_dataframe_agent(llm_dict[llm_name], df,extra_tools=custom_tool_list, verbose=False,agent_executor_kwargs={
                "handle_parsing_errors": True
            })

    template2 = custom_prefix+"""'\nYou are working with a pandas dataframe in Python. The name of the dataframe is `df`.\nYou should use the tools below to answer the question posed of you:\n\n name_search: Always use this tool, when there is a noun in the user query. Search for nouns and correct the spellings given in the query.\n\npython_repl_ast: A Python shell. Use this to execute python commands. Input should be a valid python command. When using this tool, sometimes output is abbreviated - make sure it does not look abbreviated before using it in your answer.\n \nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [python_repl_ast]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\n\nThis is the result of `print(df.head())`:\n{df_head}\n\nBegin!\nQuestion: {input},'Think if bar or line charts help in answering the question better. If yes, generate the charts, irrespective of that, answer with a text.\n{agent_scratchpad}"""+custom_suffix

    agent.agent.llm_chain.prompt.template = template2


    return agent


def query_agent(agent, query):
    """
    Query an agent and return the response as a string.

    Args:
        agent: The agent to query.
        query: The query to ask the agent.

    Returns:
        The response from the agent as a string.
    """
    mixed_output = []

    # Run the prompt through the agent.
    response = agent.run(query)

    # Save the plot to an in-memory buffer
    plot_buffer = io.BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)

    mixed_output.append(plot_buffer.getvalue())

    # Convert the response to a string.
    return {"string":response.__str__(),"stdout":mixed_output}