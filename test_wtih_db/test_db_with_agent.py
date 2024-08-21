from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentType
from langchain_ollama.llms import OllamaLLM


model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")

db = SQLDatabase.from_uri( f"postgresql+psycopg2://postgres:123@localhost:5432/tharo_db", sample_rows_in_table_info = 3)

agent_executor = create_sql_agent(model, db = db, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose = True)

print("Loading ...")
agent_executor.invoke({"input" : "Which class that have high number of students"})