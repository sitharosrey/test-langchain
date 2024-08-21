# from langchain.agents import AgentExecutor, create_react_agent
# from langchain_core.tools import Tool
# from langchain import hub
# from langchain_community.utilities import SQLDatabase
# from langchain_ollama.llms import OllamaLLM
# from langchain.chains import create_sql_query_chain
#
# db = SQLDatabase.from_uri(
#     f"postgresql+psycopg2://postgres:123@localhost:5432/tharo_db",
# )
# model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")
#
#
# def create_query(*args, **kwargs):
#     write_query = create_sql_query_chain(model, db)
#     return write_query
#
#
# tools = [
#     Tool(
#         name="CreateQuery",
#         func=create_query,
#         description="Create a SQL query chain",
#     ),
# ]
#
# prompt = hub.pull("hwchase17/react", api_key="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")
#
# my_agent = create_react_agent(llm=model, tools=tools, prompt=prompt, stop_sequence=True)
#
# agent_executor = AgentExecutor.from_agent_and_tools(
#     agent=my_agent,
#     tools=tools,
#     verbose=True
# )
#
# response = agent_executor.invoke({"input": "Which class that have high number of students"})
#
# print(response)
