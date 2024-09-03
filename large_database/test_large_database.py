from typing import List
from operator import itemgetter

from langchain_groq import ChatGroq
from langchain.chains import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

print(GROQ_API_KEY)

db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:123@localhost:5432/virtual_biz_db",
                          sample_rows_in_table_info=3)

# model = ChatOllama(model="llama3.1:8b-instruct-q5_0")
model = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama3-70b-8192")


class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")


def get_tables(tables: List[Table]) -> List[str]:
    tables_for_return = []
    for table in tables:
        tables_for_return.append(table.name)

    return tables_for_return


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

table_chain = prompt | llm_with_tools | output_parser | get_tables

print("Loading ...")

result = table_chain.invoke({"input": "how many product in tharo shop"})

print(result)

query_chain = create_sql_query_chain(model, db)
# Convert "question" key to the "input" key expected by current table_chain.
table_chain = {"input": itemgetter("question")} | table_chain

print("table_chain : ", result)

# Set table_names_to_use using table_chain.
full_chain = RunnablePassthrough.assign(table_names_to_use=table_chain) | query_chain

print("full_chain : ", full_chain)

query = full_chain.invoke(
    {"question": "how many product in tharo shop"}
)

print(query)