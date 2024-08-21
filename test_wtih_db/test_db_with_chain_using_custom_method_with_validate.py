from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase

# Setup and connect to the database
db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:123@localhost:5432/tharo_db")

# Initialize the model
model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")


# this function use to execute a chain with retries
def execute_chain(chain, input_data, retries=3):
    for _ in range(retries):
        result = chain.invoke(input_data)
        print("this is result : ", result)
        if result:
            return result
    print("Failed to get a valid response after multiple attempts.")
    return None


# this function use to generate sql query
def generate_sql_query(question):
    prompt_template = """You are a SQL expert of {dialect}. 
    Please write an SQL query base on this question: "{question}" and pay attention to use only the column names you can see in the tables below.
    Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    
    Here is database information: {schema_info}.
    
    Only provide the SQL script without any explanation."""

    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | model | StrOutputParser()

    input_data = {
        "dialect": db.dialect,
        "schema_info": db.get_table_info(),
        "question": question
    }

    return execute_chain(chain, input_data)


# this function use to validate and correct the sql query
def validate_sql_query(query_result):
    validate_template = """Here is the query to check: "{query_result}"

    Please ensure the query is executable. If there are any mistakes or incorrect column names, 
    correct them and rewrite the query. 
    
    Please use only this database information: {schema_info}

    Output the final SQL query in this format:
    Final SQL query: "Output here"
    """

    validate_prompt = ChatPromptTemplate.from_template(validate_template)
    validate_chain = validate_prompt | model | StrOutputParser()

    input_data = {
        "query_result": query_result,
        "schema_info": db.get_table_info()
    }

    return execute_chain(validate_chain, input_data)


# call the first method to generate the query
query_result = generate_sql_query("how many students in each class")

print("this is query_result: ", query_result)

# check the response, if we got response then take that to validate
if query_result:
    final_result = validate_sql_query(query_result)

    # check the response from validate, if got it, then print it out
    if final_result:
        print("Final Result:", final_result)