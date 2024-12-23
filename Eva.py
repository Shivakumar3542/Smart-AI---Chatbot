import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure Generative AI model
genai.configure(api_key="AIzaSyAdRw5RBVvuch-aYoXa0aOS3NHYOKPrJ1Q")

sys_prompt = """You are Eva, a friendly and helpful personal assistant. Start every interaction with a warm greeting like: 
                "Hi, my name is Eva, your personal assistant! How can I assist you today?"
                
                Your primary goal is to help the user by addressing their queries in a simple, clear, and effective manner. Maintain a conversational and approachable tone throughout the interaction to make the user feel comfortable.
                
                For each query:
                1. Begin with a concise and generalized explanation.
                2. If the user asks for more details, provide a more in-depth response, ensuring it's easy to understand.
                3. Avoid overly complex or technical jargon unless the user specifically requests it.
                
                Always stay polite and supportive, making the user feel valued. If a query falls outside your expertise, acknowledge it politely and redirect the user back to the areas you can assist with. 
                
                End conversations with a kind note or a helpful offer, such as: 
                "Let me know if there’s anything else I can help you with!"
                """


llm = genai.GenerativeModel("models/gemini-1.5-flash", system_instruction = sys_prompt)

# Load and display the image
image = Image.open("evaa.jpg")

# Initialize chat history and model
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chatbot = llm.start_chat(history=[])

# Set up page layout with title
st.set_page_config(page_title="Smartbot Assistant", page_icon="🤖", layout="wide")

st.image(image)

# Sidebar - Chat history
with st.sidebar:
    st.title("Chat History")
    if st.session_state.chat_history:
        for i, (role, text) in enumerate(st.session_state.chat_history):
            st.write(f"**{i + 1}. {role.capitalize()}**: {text}")

# Chat message input field
User_prompt = st.chat_input("Ask me anything...")

# Process user input and generate AI response
if User_prompt:
    # Append user message to chat history
    st.session_state.chat_history.append(("User", User_prompt))
    st.chat_message("User").write(User_prompt)

    # Generate AI response
    response = chatbot.send_message(User_prompt)
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
