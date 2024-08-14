import os 
from openai import OpenAI

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY is not set") 

client = OpenAI()

def get_chatgpt_response(prompt:str):
    """ Get response from chatgpt model in stream mode"""
    stream = client.chat.completions.create(
         model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": prompt}],
        temperature=0.3,
        stream=True,
        max_tokens=4096
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content