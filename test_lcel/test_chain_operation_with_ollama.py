from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import StrOutputParser

template = """Tell me about {topic} in Cambodia in short."""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3.1:8b-instruct-q5_0")

# this line mean it take the input from invoke method and then pass to prompt then pass to model
# and then take the final output from model to StrOutputParser to structure the response, this is how LCEL work
chain = prompt | model | StrOutputParser()

print("loading ...")
result = chain.invoke({"topic": "People"})
print("result ", result)