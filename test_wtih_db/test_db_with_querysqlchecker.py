from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
from langchain_groq import ChatGroq

import os


load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

print(GROQ_API_KEY)

# Setup and connect to the database
db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:123@localhost:5432/virtual_biz_db",
                          sample_rows_in_table_info=3)

model = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama3-70b-8192")

db_chain = SQLDatabaseChain.from_llm(model, db, verbose=True)
output = db_chain.invoke({"query" : "Find all information of product in tharo shop"})

print(output['result'])