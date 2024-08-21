from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase

# Setup db and connect db
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:123@localhost:5432/tharo_db",
)

template = """You are a SQL expert of {dialect}. 
Please write an SQL query base on this question: "{question}" and pay attention to use only the column names you can see in the tables below.
Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Here is database information: {schema_info}.

Only provide the SQL script without any explanation."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")

chain = prompt | model | StrOutputParser()

print("loading ... ")
query_result = None

# retry 3 time if the model cannot provide the response
for _ in range(3):
    query_result = chain.invoke({
        "dialect": db.dialect,
        "schema_info": db.get_table_info(),
        "question": "how many students in each class"
    })
    if query_result:
        break

if not query_result:
    print("Failed to get a valid response after 3 attempts.")
else:
    print("Query Result:", query_result)
    print("done ...")

# validate the query with another prompt
validate_template = """
Here is the query to check: "{query_result}"

Please double check and make sure the query can execute well, if there are any mistakes or incorrect column name please correct it then rewrite the query, following only this database information: {schema_info}

Output the final SQL query only and for the output, please following this format:
Final SQL query: "output here"
"""

validate_prompt = ChatPromptTemplate.from_template(validate_template)

print(validate_prompt.format(query_result=query_result, schema_info=db.get_table_info()))

validate_chain = validate_prompt | model | StrOutputParser()

print("loading ... ")
final_result = None

for _ in range(3):
    final_result = validate_chain.invoke({"query_result": query_result,
                                          "schema_info": db.get_table_info()})
    if final_result:
        break

if not final_result:
    print("Failed to get a valid response after 3 attempts.")
else:
    print("final_result:", final_result)
    print("done ...")