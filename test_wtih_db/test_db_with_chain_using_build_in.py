from langchain_ollama.llms import OllamaLLM
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain

# Setup db and connect db
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:123@localhost:5432/tharo_db",
)

model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")

chain = create_sql_query_chain(model, db)

# we can use this to get prompt from create_sql_query_chain
# https://python.langchain.com/v0.2/docs/how_to/sql_prompting/
print("this is prompt : ", chain.get_prompts()[0].pretty_print())

print("loading ...")
response = chain.invoke({"question": "List class that have the most number of students"})
print("response : ", response)

# we can handle exception here, if we want
if response is not None:
    result = (db.run(response))
    print(result)
else:
    print("Cannot generate the query, please change modify your question.")
