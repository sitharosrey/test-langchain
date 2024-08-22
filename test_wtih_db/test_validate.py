from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

import os

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

print(GROQ_API_KEY)
print("Loading ...")

# Setup and connect to the database
db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:123@localhost:5432/virtual_biz_db",
                          sample_rows_in_table_info=3)

model = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama3-70b-8192")


def generate_query_and_test_query(llm_model, question, database, check_query=False):
    prompt_template = """You are a SQL expert of {dialect}. 
       Please write an SQL query base on this question: "{question}" and pay attention to use only the column names you can see in the tables below.
       Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table and if you use the SELECT with GROUP BY, please check it because if it not appear in group by it will got error.

       Here is database information: {schema_info}

       Only provide the SQL script without any explanation and follow this format for output: 
       SQL Script: <<Output here>>
       """

    input_data = {
        "dialect": database.dialect,
        "schema_info": database.get_table_info(),
        "question": question
    }

    prompt = ChatPromptTemplate.from_template(prompt_template)
    while True:
        count = 0
        chain = prompt | llm_model | StrOutputParser()

        response_query = chain.invoke(input_data)
        if response_query or count > 3:
            # execute the query to database, and if error retry again
            if response_query and check_query is False:
                    print("this is in the try catch")
                    final_query = response_query.strip().replace("SQL Script: ", "")
                    print("this is final_query : ", final_query)

                    try:
                        data = database.run(final_query.strip())
                        print("data : ", data)
                    except Exception as e:
                        # I want to implement the memory here, base on the that regenerate again
                        print("Cannot execute query and here is the error : ", e)
            break
        count += 1
    return response_query


print(generate_query_and_test_query(model, "List all products in tharo shop", db))
