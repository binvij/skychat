import os
import requests 
import streamlit as st



with st.sidebar:
	st.header("About SkyChat")
	st.markdown(
        """
        **SkyChat** is an **AI Enabled Assistant**, which can help answers your doubts/queries relating to skydiving principles and fundamentals. 
        """
		)


st.title("SkyChat")


#initiliaze chat history 
if "messages" not in st.session_state:
	st.session_state.messages = []

# display chat message from history on app rerun
for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])


# react to user input 
if prompt := st.chat_input("Please ask?"):
	# display user message in chat message container 
	with st.chat_message("user"):
		st.markdown(prompt)

	# add user message to chat history
	st.session_state.messages.append({"role": "user", "content": prompt})
	data = {"name": "user", "query": prompt}

	with st.spinner("searching for answer..."):
		resp = requests.post("https://skybotapi.azurewebsites.net/bot/v1/ask", json= data)
		output_text = ""
		if resp.status_code == 200:
			output_text = resp.json()["response"]
		else:
			output_text = "I am unable to find the answer for the question. Could you try rephrase the question?"
			st.chat_message("assistant").markdown(output_text)


		with st.chat_message("assistant"):
			st.markdown(output_text)
			st.session_state.messages.append({"role":"assistant", "content": output_text})



