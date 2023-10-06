import openai
import streamlit as st

# set api key
openai.api_key = st.secrets["pass"]

st.header ("Text to SQL generator using OpenAi")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



# def continue_conversation(messages, temperature=0):
#     """
#     Continue a conversation using the OpenAI GPT-3 model.

#     Args:
#         messages (list): List of message objects containing role and content.
#         temperature (float): Sampling temperature for response generation.

#     Returns:
#         str: The response message content.
#     """
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#         temperature=temperature,
#     )
#     return response.choices[0].message["content"]


context = [{'role': 'system', 'content': """
            You are an SQL bot designed to help users create SQL commands.\
            Your responses should begin with "This is your SQL," \
            followed by the SQL statement that fulfills the user's request. \
            Your database consists of SQL tables, and your goal is to keep SQL \
            commands straightforward. Display the SQL command in white letters\
            on a black background, followed by a brief and clear explanation of \
            how it functions. If a user requests something that cannot be \
            achieved with an SQL command, provide a polite and simple response,\
            and encourage them to ask for a SQL-related request."""}]

context.append( {'role':'system', 'content':"""
first table:
{'table name': 'eiaweeklydieselprice',
'columns': ['recordSurrogateKey', 'Week', 'PricePerGallon', 'WeeklyChange', 'YearlyChange', 'recordCreatedTimestamp'],
'data types': [StringType, DateType, DecimalType(18,3), DecimalType(18,3), DecimalType(18,3), TimestampType]}
"""
})

st.session_state.messages = context


# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})



