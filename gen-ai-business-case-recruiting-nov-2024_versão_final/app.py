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

    # Step 1: Add the user input to the conversation history
    history.append({"role": "user", "content": input_text})

    # Step 2: Call the RAG chatbot function to get the response from the model
    response, updated_history = rag_chatbot(llm, input_text, history, index)  # Assuming rag_chatbot updates history
    
    # Step 3: Add the bot response to the history
    updated_history.append({"role": "ai", "content": response})
    
    # Step 4: Create a placeholder string with the entire conversation
    conversation_placeholder = "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in updated_history])

    # Step 5: Return the updated conversation history and the conversation placeholder string
    return updated_history, conversation_placeholder


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
        avatar_images=((r"img/user.png"), (r"img/gpt.png")),
    )

    with gr.Row():
        # Text input box
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )

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
