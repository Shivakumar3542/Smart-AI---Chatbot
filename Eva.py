import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure Generative AI model
genai.configure(api_key="AIzaSyAdRw5RBVvuch-aYoXa0aOS3NHYOKPrJ1Q")
llm = genai.GenerativeModel("models/gemini-1.5-flash")

# Load and display the image
image = Image.open("evaa.jpg")

# Initialize chat history and model
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chatbot = llm.start_chat(history=[])

# Set up page layout with title
st.set_page_config(page_title="Smartbot Assistant", page_icon="🤖", layout="wide")

# # Title Section with styling
# st.markdown("""
#     <h1 style="font-family: 'Arial', sans-serif; color: #2E8B57; text-align: center;">
#         Eva - Your Smart Companion
#     </h1>
# """, unsafe_allow_html=True)

# Display AI greeting at the top
# st.chat_message("ai").write("Hi! I’m Ellie, your smart assistant. How can I assist you today?")
st.image(image)

# Sidebar - Chat history
with st.sidebar:
    st.title("Chat History")
    if st.session_state.chat_history:
        for i, (role, text) in enumerate(st.session_state.chat_history):
            st.write(f"**{i + 1}. {role.capitalize()}**: {text}")

# Chat message input field
human_prompt = st.chat_input("Ask me anything...")

# Process user input and generate AI response
if human_prompt:
    # Append user message to chat history
    st.session_state.chat_history.append(("human", human_prompt))
    st.chat_message("human").write(human_prompt)

    # Generate AI response
    response = chatbot.send_message(human_prompt)
    ai_response = response.text

    # Append AI message to chat history
    st.session_state.chat_history.append(("ai", ai_response))
    st.chat_message("ai").write(ai_response)
    
if st.button("Export Chat History"):
    if st.session_state.chat_history:
        # Write the chat history to a text file
        with open("chat_history.txt", "w") as file:
            for role, text in st.session_state.chat_history:
                file.write(f"{role.capitalize()}: {text}\n")
        # Notify user of successful export
        st.success("Chat history exported successfully!")
        
        # Provide a download button for the exported file
        with open("chat_history.txt", "rb") as file:
            st.download_button(
                label="Download Chat History",
                data=file,
                file_name="chat_history.txt",
                mime="text/plain"
            )
    else:
        st.warning("No chat history to export!")
