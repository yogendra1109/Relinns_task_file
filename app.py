import streamlit as st
import api

# Show title and description
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses an AI model to generate answers. "
    "To use this app, you need to provide a HuggingFace API key, which you can get [here](https://huggingface.co/settings/tokens)."
)

api_key = st.text_input("HuggingFace API Key", type="password")
if not api_key:
    st.info("Please add your HuggingFace API key to continue.", icon="🗝️")

# Define the API URL
API_URL = "https://api-inference.huggingface.co/models/consciousAI/question-answering-roberta-base-s-v2"

question = st.text_input("Your question", "")

if st.button("Ask"):
    if question:
        output = chat_with_gpt(question, context, api_key)
        if output:
            st.write(f"Question: {question}")
            st.write(f"Answer: {output['answer']}")
    else:
        st.warning("Please enter a question.")

# Option to exit the chat
if st.button("Exit"):
    st.stop()