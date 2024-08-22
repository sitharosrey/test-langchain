from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
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

# Initialize the model
# model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")
model = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama3-70b-8192")

# this can work with small database

# this function use to execute a chain with retries
def execute_chain(chain, input_data, retries=5):
    for _ in range(retries):
        result = chain.invoke(input_data)
        print("this is result : ", result)
        if result:
            print("I know : ", result)
            return result
    print("Failed to get a valid response after multiple attempts.")
    return None


# this function use to generate sql query
def generate_sql_query(question):
    prompt_template = """You are a SQL expert of {dialect}. 
    Please write an SQL query base on this question: "{question}" and pay attention to use only the column names you can see in the tables below.
    Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table and if you use the SELECT with GROUP BY, please check it because if it not appear in group by it will got error.
    
    Here is database information: {schema_info}.
    
    Only provide the SQL script without any explanation."""

    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | model | StrOutputParser()

    input_data = {
        "dialect": db.dialect,
        "schema_info": db.get_table_info(),
        "question": question
    }

    print(prompt.format(dialect=db.dialect,
                        schema_info=db.get_table_info(),
                        question=question))
    return execute_chain(chain, input_data)


# this function use to validate and correct the sql query
def validate_sql_query(query_result):
    validate_template = """Here is the query to check: "{query_result}"
    
    Please double check and make sure the query can execute well and if it is okay please return the original query, however if there are any mistakes or incorrect column name, please correct it then rewrite the query, following only this database information: {schema_info}
    
    Output the final SQL query only and for the output, please following this format:
    Final SQL query: "output here"
    """

    validate_prompt = ChatPromptTemplate.from_template(validate_template)
    validate_chain = validate_prompt | model | StrOutputParser()

    input_data = {
        "query_result": query_result,
        "schema_info": db.get_table_info()
    }

    return execute_chain(validate_chain, input_data)


print("Loading ...")
# call the first method to generate the query
query_result = generate_sql_query("Find all information of product in tharo shop")
print("this is query_result: ", query_result)

# check the response, if we got response then take that to validate
if query_result:
    final_result = validate_sql_query(query_result)

    # check the response from validate, if got it, then print it out
    if final_result:
        # we can take this "final_result", to run with our database
        print("Final Result:", final_result)

print("Done!")
