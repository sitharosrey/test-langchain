from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from dotenv import load_dotenv
from langchain_groq import ChatGroq

import os

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# setup and connect to the database
db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:123@localhost:5432/virtual_biz_db")

model = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama3-70b-8192")

write_query = create_sql_query_chain(model, db)

print(write_query.invoke({"question": "Find all information of product in Tamp shop"}))


# # Setup db and connect db
# db = SQLDatabase.from_uri(
#     f"postgresql+psycopg2://postgres:123@localhost:5432/tharo_db",
# )
#
# model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")
# execute_query = QuerySQLDataBaseTool(db=db)

# we can use this to get prompt from create_sql_query_chain
# https://python.langchain.com/v0.2/docs/how_to/sql_prompting/
# print("this is prompt : ", chain.get_prompts()[0].pretty_print())
# chain = write_query | execute_query

# print("loading ...")
# response = chain.invoke({"question": "How many students learn Mathematics and Physics"})
# print("response : ", response)
