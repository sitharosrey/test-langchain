from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os


load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

print(GROQ_API_KEY)

# Setup and connect to the database
# db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:123@localhost:5432/virtual_biz_db",
#                           sample_rows_in_table_info=3)
db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:123@localhost:5432/virtual_biz_db",
                          sample_rows_in_table_info=3)

# Initialize the model
# model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")
# model = ChatOllama(model="llama3.1:8b-instruct-q5_0")
model = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama3-70b-8192")

class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")

print("1. Loading ...")

table_names = "\n".join(db.get_usable_table_names())

print(table_names)

system = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables are:

{table_names}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed.
"""

print("2. Loading ...")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{input}"),
    ]
)
llm_with_tools = model.bind_tools([Table])
output_parser = PydanticToolsParser(tools=[Table])

print("3. Loading ...")

table_chain = prompt | llm_with_tools | output_parser

print("Loading ...")

result = table_chain.invoke({"input": "how many product in tharo shop"})

print(result)
print(len(result))