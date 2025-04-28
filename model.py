import requests
import _pickle
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('HUGGINGFACE_API_KEY')
if not api_key:
    raise ValueError("Please set HUGGINGFACE_API_KEY in your .env file")

def query_model(question, context):
    API_URL = "https://api-inference.huggingface.co/models/consciousAI/question-answering-roberta-base-s-v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Try to parse the response as JSON
        try:
            result = response.json()
            return result
        except json.JSONDecodeError:
            print(f"Raw response content: {response.text}")
            return {"error": "Invalid JSON response from API"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

def main():
    # Load context from pickle file
    try:
        with open("data.pkl", "rb") as f:
            loaded_data = _pickle.load(f)
        context = loaded_data.get('context', None)
        label = loaded_data.get('label', None)

        if not context:
            print("Error: No context found in data.pkl")
            return

        print("\nContext preview (first 200 characters):")
        print(context[:200] + "...\n")
        
        print("Welcome to the Python Website Chatbot!")
        print("Type 'exit' to quit the chatbot.")
        print("You can ask questions about Python based on the website content.\n")
        
        while True:
            question = input("\nEnter your question: ")
            if question.lower() == 'exit':
                print("Goodbye!")
                break
                
            print("Generating answer...")
            result = query_model(question, context)
            
            if isinstance(result, dict):
                if 'error' in result:
                    print(f"Error from API: {result['error']}")
                elif 'answer' in result:
                    print(f"Answer: {result['answer']}")
                    if 'score' in result:
                        print(f"Confidence Score: {result['score']:.4f}")
                else:
                    print(f"Unexpected API response format: {result}")
            else:
                print(f"Unexpected response type: {type(result)}")
                print(f"Response content: {result}")
            
    except FileNotFoundError:
        print("Error: data.pkl file not found")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()