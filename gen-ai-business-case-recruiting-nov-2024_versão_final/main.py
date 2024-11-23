from dotenv import load_dotenv
load_dotenv(override=True)

import faiss
from openai import AzureOpenAI
from src.services.models.embeddings import Embeddings
from src.services.vectorial_db.faiss_index import FAISSIndex
from src.ingestion.ingest_files import ingest_files_data_folder
from src.services.models.llm import LLM
import os
from dotenv import load_dotenv
import time

def rag_chatbot(llm: LLM, input_text: str, history: list, index: FAISSIndex):
    """Retrieves relevant information from the FAISS index, generates a response using the LLM, and manages the conversation history.

    Args:
        llm (LLM): An instance of the LLM class for generating responses.
        input_text (str): The user's input text.
        history (list): A list of previous messages in the conversation history.
        index (FAISSIndex): An instance of the FAISSIndex class for retrieving relevant information.

    Returns:
        tuple: A tuple containing the AI's response and the updated conversation history.
    """
    
    # Step 1: Retrieve relevant context from the FAISS index
    relevant_contexts = index.retrieve_chunks(input_text, num_chunks=3)  # Retrieve top 3 relevant chunks based on input_text
    
    # Step 2: Prepare the prompt for the LLM
    # Combine history, context, and user input to create a complete prompt
    context = "\n".join(relevant_contexts)
    
    # Format the conversation history into a string
    conversation_history = ""
    for message in history:
        conversation_history += f"{message['role'].capitalize()}: {message['content']}\n"
    
    # Combine the history, context, and user input
    prompt = f"{conversation_history}Context: {context}\nUser: {input_text}\nAssistant:"
    
    # Step 3: Get response from the LLM
    ai_response = llm.get_response(history, context, input_text)
    
    # Step 4: Update the conversation history
    updated_history = history + [{"role": "user", "content": input_text}, {"role": "assistant", "content": ai_response}]
    
    return ai_response, updated_history


def main():
    """Main function to run the chatbot."""

    embeddings = Embeddings()
    
    index = FAISSIndex(embeddings=embeddings.get_embeddings)

    try:
        index.load_index()
    except FileNotFoundError:
        raise ValueError("Index not found. You must ingest documents first.")

    llm = LLM()
    history = []
    print("\n# INTIALIZED CHATBOT #")

    while True:
        user_input = str(input("You:  "))
        if user_input.lower() == "exit":
            break
        response, history = rag_chatbot(llm, user_input, history, index)
        
        print("AI: ", response)


if __name__ == "__main__":
    main()