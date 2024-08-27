from langchain.chains.sql_database.prompt import DECIDER_PROMPT, PROMPT, SQL_PROMPTS
from langchain_community.tools.sql_database.prompt import QUERY_CHECKER
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
from langchain_groq import ChatGroq

import os

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# setup and connect to the database
db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:123@localhost:5432/virtual_biz_db")

model = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama3-70b-8192")

template = """You are a {dialect} expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {rows} results using the LIMIT clause as per {dialect}. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Only use the following tables:
{table_info}

Question: {input}
"""

prompt = ChatPromptTemplate.from_template(template)


def generate_query_and_test_query(llm_model, prompt_input, question, database, retry=3, check_query=False):
    count = 0
    chain = prompt_input | llm_model
    while True:
        print("this is count : ", count)
        count += 1

        input_data = {
            "dialect": db.dialect,
            "table_info": db.get_table_info(),
            "rows": 5,
            "input": question
        }

        response_query = chain.invoke(input_data)
        if response_query or count > retry:
            # execute the query to database, and if error retry again
            if response_query:
                if check_query is False:
                    print("this is try to generate the QUERY")
                    final_query = response_query.content.split("SQLResult:")[0].replace("SQLQuery:", "").replace("```",
                                                                                                                 "").strip()
                    print("this is final_query : ", final_query)

                    try:
                        data = database.run(final_query.strip())
                        print("data : ", data)
                    except Exception as e:
                        # in this section, the model will go try again, but not more than 3 times
                        print("Cannot execute query and here is the error : ", e)
                        continue
                else:
                    # I will implement here later
                    print("this is try to validate the QUERY")
            break
    return response_query


print(generate_query_and_test_query(llm_model=model, prompt_input=prompt,
                                    question="Which products that did not use by any shop",
                                    database=db).content)
