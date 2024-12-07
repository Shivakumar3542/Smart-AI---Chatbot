import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure Generative AI model
genai.configure(api_key="AIzaSyAdRw5RBVvuch-aYoXa0aOS3NHYOKPrJ1Q")
llm = genai.GenerativeModel("models/gemini-1.5-flash")

# Initialize chat history and model
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chatbot = llm.start_chat(history=[])

# Load and display the image (assuming the image path is correct)
#image = Image.open("Friday.png")

# Set up page layout with title and image
st.set_page_config(page_title="Smartbot Assistant", page_icon="🤖", layout="wide")

# Title Section with styling
st.markdown("""
    <h1 style="font-family: 'Arial', sans-serif; color: #2E8B57; text-align: center;">
        Welcome to Smartbot - Your Smart Assistant
    </h1>
""", unsafe_allow_html=True)

# Display image on top
#st.image(image, use_column_width=True)

# Greeting message displayed at the top
st.markdown("""
    <div style="font-size: 18px; font-family: 'Arial', sans-serif; color: #555555; text-align: center;">
        Hello! I'm Friday, your smart AI assistant. How can I assist you today?
    </div>
""", unsafe_allow_html=True)

# Chat message input field
human_prompt = st.text_input("Ask me anything...")

# Sidebar - Chat history
with st.sidebar:
    st.title("Chat History")
    if st.session_state.chat_history:
        for idx, (role, text) in enumerate(st.session_state.chat_history):
            message = f"**{role.capitalize()}**: {text}"
            st.write(f"{idx + 1}. {message}")

# Process user input and generate AI response
if human_prompt:
    # Append human message to history
    st.session_state.chat_history.append(("human", human_prompt))
    st.markdown(f"**You**: {human_prompt}")

    # Generate AI response
    response = chatbot.send_message(human_prompt)
    ai_response = response.text

    # Append AI response to history and display
    st.session_state.chat_history.append(("ai", ai_response))
    st.markdown(f"**AI**: {ai_response}")

