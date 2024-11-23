'''from main import rag_chatbot
import gradio as gr
import time

from src.ingestion.ingest_files import ingest_files_data_folder
from src.services.models.embeddings import Embeddings
from src.services.models.llm import LLM
from src.services.vectorial_db.faiss_index import FAISSIndex

# Initialize instances for the LLM, embeddings, and FAISS index
llm = LLM()
embeddings = Embeddings()
index = FAISSIndex(embeddings=embeddings.get_embeddings)

# Load the FAISS index, ingest data if it doesn't exist
try:
    index.load_index()
except FileNotFoundError:
    ingest_files_data_folder(index)
    index.save_index()


def chatbot_wrapper(input_text, history):
    """
    Wrapper function for the chatbot, handling Gradio integration.

    Args:
        input_text (str): User input text.
        history (list): Conversation history.

    Returns:
        tuple: Updated conversation history and a placeholder string.
    """
    if history is None:
        history = []

    _, updated_history = rag_chatbot(llm, input_text, history[:-1], index) # Call the main chatbot function with previous history.

    return updated_history, ""  # Return updated history and empty string.


def add_user_text(history, txt):
    """
    Adds user text to the conversation history.

    Args:
        history (list): Conversation history.
        txt (str): User input text.

    Returns:
        tuple: Updated conversation history and user input text.
    """
    if history is None:
        history = []
    history = history + [{"role": "user", "content": txt}]
    return history, txt


def update_temperature(temperature):
    """Placeholder function for updating temperature."""
    # Not Implemented
    return temperature


def update_max_tokens(max_tokens):
    """Placeholder function for updating max tokens."""
    # Not Implemented
    return max_tokens


def add_file(history, file_obj):
    """Placeholder function for handling file uploads."""
    return history


def process(history):
    """Placeholder function for processing input."""
    return history


# Custom CSS for styling the chatbot
custom_css = """
#chatbot {
    height: 70vh !important;
}
"""

# Create the Gradio interface
with gr.Blocks(css=custom_css) as demo:
    # Chatbot UI element
    chatbot_ui = gr.Chatbot(
        [],
        type="messages",
        elem_id="chatbot",
        bubble_full_width=True,
        height=800,
        ##avatar_images=((r"img/user.png"), (r"img/gpt.png")),
    )

    with gr.Row():
        # Text input box
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        file_input = gr.File(label="Faça upload de um ou mais arquivos")

    with gr.Row():
        # Sliders for temperature and max tokens
        temperature = gr.Slider(0.0, 2, value=1, label="Temperature")
        max_tokens = gr.Slider(1, 1000, value=800, label="Max Tokens")

    # Register slider values (currently placeholder functions)
    t = temperature.release(update_temperature, inputs=[temperature])
    mt = max_tokens.release(update_max_tokens, inputs=[max_tokens])

    # Define the event chain: submit text -> add to history -> call chatbot_wrapper -> clear textbox
    txt_msg = txt.submit(add_user_text, [chatbot_ui, txt], [chatbot_ui, txt]).then(
        chatbot_wrapper, [txt, chatbot_ui], [chatbot_ui, txt], queue=False
    ).then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)


# Launch the Gradio interface
demo.launch()
'''
from main import rag_chatbot
import gradio as gr
import time

from src.ingestion.ingest_files import ingest_files_data_folder
from src.services.models.embeddings import Embeddings
from src.services.models.llm import LLM
from src.services.vectorial_db.faiss_index import FAISSIndex

# Initialize instances for the LLM, embeddings, and FAISS index
llm = LLM()
embeddings = Embeddings()
index = FAISSIndex(embeddings=embeddings.get_embeddings)

# Load the FAISS index, ingest data if it doesn't exist
try:
    index.load_index()
except FileNotFoundError:
    ingest_files_data_folder(index)
    index.save_index()


def chatbot_wrapper(input_text, history):
    """
    Wrapper function for the chatbot, handling Gradio integration.

    Args:
        input_text (str): User input text.
        history (list): Conversation history.

    Returns:
        tuple: Updated conversation history and a placeholder string.
    """
    if history is None:
        history = []

    _, updated_history = rag_chatbot(llm, input_text, history[:-1], index)  # Call the main chatbot function with previous history.

    return updated_history, ""  # Return updated history and empty string.


def add_user_text(history, txt):
    """
    Adds user text to the conversation history.

    Args:
        history (list): Conversation history.
        txt (str): User input text.

    Returns:
        tuple: Updated conversation history and user input text.
    """
    if history is None:
        history = []
    history = history + [{"role": "user", "content": txt}]
    return history, txt


def update_temperature(temperature):
    """Placeholder function for updating temperature."""
    # Not Implemented
    return temperature


def update_max_tokens(max_tokens):
    """Placeholder function for updating max tokens."""
    # Not Implemented
    return max_tokens


def add_file(history, file_obj):
    """Placeholder function for handling file uploads."""
    return history


def process(history):
    """Placeholder function for processing input."""
    return history

# Custom CSS for improved ChatGPT-style layout
custom_css = """
body {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
    background-image: url('gen-ai-business-case-recruiting-nov-2024_versão_final/img/1.png'); 
    background-size: cover; /* Ensure the image covers the entire background */
    background-position: center; /* Center the image */
    background-repeat: no-repeat; /* Prevent the image from repeating */
}

#chatbot {
    height: 80vh !important; /* Chatbot window height */
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 10px;
    overflow-y: auto;
    background-color: white;
}

#input-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background-color: white;
    border-top: 1px solid #e0e0e0;
    gap: 8px;
}

#write-bar {
    flex: 0.95; /* Input bar takes up 95% of the space */
    padding: 10px;
    border: 1px solid #e0e0e0;
    border-radius: 20px;
    font-size: 14px;
}

#send-button {
    flex: 0.05; /* Send button takes up 5% of the space */
    height: 40px;
    background-color: #10a37f;
    color: white;
    border: none;
    border-radius: 50%;
    font-size: 12px;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    min-width: 40px; /* Ensure a minimum clickable size */
}

#menu-button {
    position: fixed; /* Position it outside the layout */
    bottom: 15px; /* Move to bottom */
    left: 15px; /* Move to left */
    background-color: #e0e0e0;
    border: none;
    border-radius: 50%;
    height: 40px;
    width: 40px;
    text-align: center;
    font-size: 18px;
    cursor: pointer;
    z-index: 1000; /* Ensure it stays on top */
}
#chatbot-header {
    position: fixed; /* Position ChatBot text fixed at top left */
    top: 10px;
    left: 15px;
    font-size: 24px;
    font-weight: bold;
    color: #333;
    z-index: 1000; /* Ensure it stays on top */
}
"""

import gradio as gr
from main import rag_chatbot

def chatbot_wrapper(input_text, history):
    if history is None:
        history = []

    _, updated_history = rag_chatbot(llm, input_text, history[:-1], index)
    return updated_history, ""

def add_user_text(history, txt):
    if history is None:
        history = []
    history = history + [{"role": "user", "content": txt}]
    return history, txt

# Create Gradio Blocks interface
with gr.Blocks(css=custom_css) as demo:
    # Sidebar menu button (outside layout)
    gr.Button("≡", elem_id="menu-button")
    # ChatBot Header (ChatBot text at the top-left corner)
    gr.HTML("<div id='chatbot-header'>ChatBot</div>")
    # Chatbot conversation window
    chatbot_ui = gr.Chatbot(
        [], 
        type="messages", 
        elem_id="chatbot"
    )

    # Input bar and send button row
    with gr.Row(elem_id="input-row"):
        txt = gr.Textbox(
            show_label=False, 
            placeholder="Type your message...", 
            elem_id="write-bar"
        )
        send_button = gr.Button("⏎", elem_id="send-button")

    # Text submission logic
    txt.submit(add_user_text, [chatbot_ui, txt], [chatbot_ui, txt]).then(
        chatbot_wrapper, [txt, chatbot_ui], [chatbot_ui, txt], queue=False
    ).then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)

    # Button click logic: when the send button is pressed
    send_button.click(add_user_text, [chatbot_ui, txt], [chatbot_ui, txt]).then(
        chatbot_wrapper, [txt, chatbot_ui], [chatbot_ui, txt], queue=False
    ).then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)

# Launch the interface
demo.launch()

