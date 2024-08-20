from langchain_core.runnables import RunnableLambda

def add_two(x):
    return x+2

def minus_one(x):
    return x-1

add_two = RunnableLambda(add_two)
minus_one = RunnableLambda(minus_one)

chain = add_two | minus_one
result = chain.invoke(3)

print(result)