from dotenv import load_dotenv
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool, QuerySQLCheckerTool
from langchain_groq import ChatGroq

import os

load_dotenv()

# Setup db and connect db
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:123@localhost:5432/tharo_db",
)

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# setup and connect to the database
db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:123@localhost:5432/virtual_biz_db")

model = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama3-70b-8192")

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(model, db)

# chain = prompt | model | StrOutputParser() | execute_query

def parseResponseToSQL(response):
    print(response)
    return response.strip().replace("```", "").replace("SQLQuery:", "")

chain = write_query | parseResponseToSQL | execute_query

result = chain.invoke({"question": "how many category"})

print("result : ", result)