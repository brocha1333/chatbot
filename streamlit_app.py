import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")

openai_api_key = st.secrets["api_key"] 
# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

prompt = st.chat_input("What is up?")
#if prompt==None:
#   st.stop()

#with st.chat_message("user"):
#   st.markdown(prompt)

# Generate a response using the OpenAI API.

#stream = client.chat.completions.create(
#        model="gpt-4o-mini",  
#        messages=[
#            {"role": "system", "content": "You are an assistant."},
#            {"role": "user", "content": prompt}
#        ],
#        max_tokens=800,
#        temperature=0,
#    )
#respuesta = stream.choices[0].message.content

#with st.chat_message("assistant"):
#   st.write(respuesta)
