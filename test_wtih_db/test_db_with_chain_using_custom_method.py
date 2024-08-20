from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase

# Setup db and connect db
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:123@localhost:5432/tharo_db",
)

template = """You are a SQL expert of {dialect}. Please write an SQL query base on this 
question {question}, following only this schema information {schema_info}. Only provide the SQL 
script without any explanation."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")

chain = prompt | model | StrOutputParser()

# not handle yet, when model cannot provide the response
print("loading ... ")
result = chain.invoke({"dialect": db.dialect,
                       "schema_info": db.get_table_info(),
                       "question": "List top 3 students base on their score"})

print("result : ", db.run(result))