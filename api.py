import requests
import os
import _pickle
import time

# Define the API URL and headers
API_URL = "https://api-inference.huggingface.co/models/consciousAI/question-answering-roberta-base-s-v2"
if 'API_KEY' in os.environ:
    api_key = os.getenv('API_KEY')
else:
    api_key = str(input('Enter HF API KEY:'))

if not api_key:
    raise ValueError("API_KEY environment variable is not set")
headers = {"Authorization": api_key}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def chat_with_gpt(question, context):
    try:
        output = query({
            "inputs": {
                "question": question,
                "context": context,
            },
        })
    except Exception as e:
        print("An error occurred:", e)
        return None

    if 'estimated_time' in output:
        print(f"Model loading, {output['estimated_time']} sec", output)
        time.sleep(output['estimated_time'])
        print('Model Running')
        output = query({
            "inputs": {
                "question": question,
                "context": context,
            },
        })
    return output

question = "what is BotPenguin?"

with open("Web-Chatbot/data.pkl", "rb") as f:
    loaded_data = _pickle.load(f)
context = loaded_data.get('context', None)

output = chat_with_gpt(question, context)

# Generating answer and print the result
try:
    print(question, '\n', "Generating answer: ", output["answer"])
except Exception as e:
    print("An error occurred while generating the answer:", e)

while True:
    question = input("Ask a question or exit: ")
    if question.lower() == 'exit':
        break
    try:
        output = chat_with_gpt(question, context)
        if output:
            print(f"Generating answer: {output['answer']}\n\n", end='')
        else:
            print("No output received from the model.")
    except Exception as e:
        print("An error occurred:", e)