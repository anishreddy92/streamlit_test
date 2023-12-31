import streamlit as st
import pandas as pd
import json
from agent import query_agent, create_agent
from langchain.callbacks import get_openai_callback


from PIL import Image
import io


# Function to check if the data represents an image (plot)
def is_image(data):
    try:
        Image.open(io.BytesIO(data))
        return True
    except (IOError, SyntaxError):
        return False



def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    return json.loads(response)


def write_response(response: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # # Check if the response is an answer.
    # if "answer" in response_dict:
    #     st.write(response_dict["answer"])

    # # Check if the response is a bar chart.
    # if "bar" in response_dict:
    #     data = response_dict["bar"]
    #     df = pd.DataFrame(data)
    #     df.set_index("columns", inplace=True)
    #     st.bar_chart(df)

    # # Check if the response is a line chart.
    # if "line" in response_dict:
    #     data = response_dict["line"]
    #     df = pd.DataFrame(data)
    #     df.set_index("columns", inplace=True)
    #     st.line_chart(df)

    # Check if the response is a table.
    # if "table" in response_dict:
    #     data = response_dict["table"]
    #     df = pd.DataFrame(data["data"], columns=data["columns"])
    #     st.table(df)

    st.write(response["string"])

    mixed_stdout = response["stdout"]

    for data in mixed_stdout:
        if is_image(data):
            st.image(data, use_column_width=True)


model_option=st.selectbox(label="Select the model", options=["gpt-35-turbo","gpt-3.5-turbo-1106","llm_gpt35_instruct"], args=None, kwargs=None,  placeholder="Choose an option", disabled=False, label_visibility="visible")

st.title("👨‍💻 Chat with your CSV")

prompt_suffix = st.text_input('Prompt Suffix')
prompt_prefix = st.text_input('Prompt prefix')

#st.write("Please upload your CSV file below.")

#data = st.file_uploader("Upload a CSV")

data = "data.csv"
query = st.text_area("Insert your query")

if st.button("Submit Query", type="primary"):
    # Create an agent from the CSV file.
    agent = create_agent(data,model_option,prompt_suffix,prompt_prefix)

    print(model_option)

    with get_openai_callback() as cb:
        # Query the agent.
        response = query_agent(agent=agent, query=query)
        st.write(f"Total Cost : Rupees {cb.total_cost*83}")
    # Decode the response.
    #decoded_response = decode_response(response)

    # Write the response to the Streamlit app.
    write_response(response)
