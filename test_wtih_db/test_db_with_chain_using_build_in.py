from langchain_ollama.llms import OllamaLLM
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool


# Setup db and connect db
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:123@localhost:5432/tharo_db",
)

model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")


# we can use this to get prompt from create_sql_query_chain
# https://python.langchain.com/v0.2/docs/how_to/sql_prompting/
# print("this is prompt : ", chain.get_prompts()[0].pretty_print())

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(model, db)

chain = write_query | execute_query

print("loading ...")
response = chain.invoke({"question": "How many students learn Mathematics and Physics"})
print("response : ", response)
