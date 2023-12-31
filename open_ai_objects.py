from langchain.chat_models import ChatOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import OpenAI

# Creating gpt 3.5  OpenAI object
llm_gpt35 = ChatOpenAI(temperature=0,
model_name="gpt-3.5-turbo"
)

llm_gpt35_1106 = ChatOpenAI(temperature=0,
model_name="gpt-3.5-turbo-1106")

llm_gpt35_instruct = OpenAI(temperature=0,
model_name="gpt-3.5-turbo-instruct")

# Create an OpenAI object
llm_gpt4 = ChatOpenAI(
temperature=0,
model_name="gpt-4"
)



llm_dict = {"gpt-3.5-turbo" : llm_gpt35
            ,"gpt-4" : llm_gpt4
            ,"gpt-3.5-turbo-1106" : llm_gpt35_1106
            ,"llm_gpt35_instruct":llm_gpt35_instruct}
