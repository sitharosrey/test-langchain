from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_community.utilities import SQLDatabase
import psycopg2

template = """You are a SQL expert of Postgres. Please write an SQL query base on this 
question {question}, following this schema information {schema_info}. Only provide 
the SQL script without any explanation and please generate sql query with the field that have in tables."""

prompt = ChatPromptTemplate.from_template(template)

# Setup database
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:123@localhost:5432/tharo_db",
)

schema_info = db.get_table_info()

print(schema_info)

# # Initialize the model with the specified version of LLaMA
# model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")
#
# # Create a chain by piping the prompt to the model
# chain = prompt | model
#
# # Function to execute the query with retry logic
# def execute_query_with_retry(query, retries=3, delay=2):
#     for attempt in range(retries):
#         try:
#             result = db.run(query)
#             return result
#         except psycopg2.Error as e:
#             print(f"Error executing query: {e}")
#             if attempt < retries - 1:
#                 print(f"Retrying in {delay} seconds...")
#             else:
#                 print("Max retries reached. Query failed.")
#                 return None
#
# # Generate the SQL query using the LLaMA model
# result = chain.invoke({
#     "schema_info": schema_info,
#     "question": "Count the number of students for each course"
# })
#
# print("Generated SQL Query: ", result)
#
# # Execute the generated SQL query with retry logic
# query_result = execute_query_with_retry(result)
#
# print("Query Result: ", query_result)

# Create a cursor object
# cursor = conn.cursor()
#
# # Fetch table information
# cursor.execute("""
# WITH table_info AS (
#     SELECT
#         table_name,
#         string_agg(column_name, ', ') AS fields
#     FROM
#         information_schema.columns
#     WHERE
#         table_schema = 'public'  -- Adjust schema if necessary
#     GROUP BY
#         table_name
# ),
# formatted_table_info AS (
#     SELECT
#         table_name || ' (' || fields || ')' AS formatted_info,
#         row_number() OVER () AS rn
#     FROM
#         table_info
# )
# SELECT
#     string_agg(formatted_info, ', ') ||
#     CASE
#         WHEN COUNT(*) > 1 THEN ' and ' ||
#              (SELECT formatted_info FROM formatted_table_info WHERE rn = (SELECT MAX(rn) FROM formatted_table_info))
#         ELSE ''
#     END AS table_info
# FROM
#     formatted_table_info
# """)
#
# # Fetch all results from the cursor
# results_of_tables_info = cursor.fetchall()
#
# # Convert the list of tuples into a raw text string
# table_information = ', '.join(row[0] for row in results_of_tables_info)
#
# # Check if table_information is empty
# if not table_information:
#     print("No table information found.")
#     cursor.close()
#     conn.close()
#     exit()
#
# # Fetch relationship information
# cursor.execute("""
# SELECT
#     'Table ' || table_name || ' has a relationship with ' || STRING_AGG('table ' || related_table, ', ') AS relationship_description
# FROM (
#     SELECT
#         tc.table_name,
#         ccu.table_name AS related_table
#     FROM
#         information_schema.table_constraints AS tc
#     JOIN
#         information_schema.key_column_usage AS kcu
#         ON tc.constraint_name = kcu.constraint_name
#     JOIN
#         information_schema.constraint_column_usage AS ccu
#         ON ccu.constraint_name = tc.constraint_name
#     WHERE
#         tc.constraint_type = 'FOREIGN KEY'
#         AND tc.table_schema = 'public'  -- Ensure it is the correct schema
#     ORDER BY
#         tc.table_name, ccu.table_name
# ) AS subquery
# GROUP BY
#     table_name
# ORDER BY
#     table_name;
# """)
#
# # Fetch results
# relationships = cursor.fetchall()
#
# # Format the results into a single string
# relationship_of_each_table_information = ', '.join(row[0] for row in relationships)
#
# # Check if relationship_of_each_table_information is empty
# if not relationship_of_each_table_information:
#     print("No relationship information found.")
#     cursor.close()
#     conn.close()
#     exit()
#
# # Define the template for the prompt
# template = """You are a SQL expert of Postgres. Based on the table information: {table_information} and relationships:
# {relationship_of_each_table_information}, write an SQL query for the following: {question}. Only provide the
# SQL script without any explanation."""
#
# # Create a prompt object from the template
# prompt = ChatPromptTemplate.from_template(template)
#
# # Initialize the model with the specified version of LLaMA
# model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")
#
# # Create a chain by piping the prompt to the model
# chain = prompt | model
#
# print("prompt : ", prompt)
#
#
# # Function to handle the result with loading
# def get_result():
#     max_retries = 5
#     for attempt in range(max_retries):
#         try:
#             print("Loading...")  # Show loading message
#             result = chain.invoke({
#                 "table_information": table_information,
#                 "relationship_of_each_table_information": relationship_of_each_table_information,
#                 "question": "Retrieve top 3 course information base on number of student enrolled"
#             })
#
#             # Check if result is not empty
#             if result:
#                 # Remove backticks from the result
#                 result = result.replace('`', '')
#                 print("Loading complete!")  # Loading complete message
#                 return result  # Return the cleaned result
#             else:
#                 print(f"Result is empty on attempt {attempt + 1}.")
#
#         except Exception as e:
#             print(f"Attempt {attempt + 1} failed: {e}")
#
#         # Wait before retrying (optional, can be added if needed)
#         if attempt < max_retries - 1:
#             print("Retrying...")
#
#     # After all retries, if no valid result
#     print("All attempts failed.")
#     return None  # Return None if all attempts fail
#
#
# # Function to execute the query and handle exceptions
# def execute_query():
#     max_retries = 3
#     for attempt in range(max_retries):
#         try:
#             result = get_result()
#             if result:
#                 print("Executing query:", result)
#                 cursor.execute(result)
#                 # Fetch results
#                 results = cursor.fetchall()
#                 print("Query results:", results)
#                 return
#             else:
#                 print("No result generated after retries.")
#                 return
#         except Exception as e:
#             print(f"Query execution failed on attempt {attempt + 1}: {e}")
#
#         # Wait before retrying (optional, can be added if needed)
#         if attempt < max_retries - 1:
#             print("Retrying query execution...")
#
#     print("All query execution attempts failed. Please try to change your question.")
#
#
# # Run the function to execute the query
# execute_query()
#
# # Close the cursor and connection
# cursor.close()
# conn.close()
