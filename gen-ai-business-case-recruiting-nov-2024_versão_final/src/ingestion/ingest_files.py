import os
from src.services.vectorial_db.faiss_index import FAISSIndex
from src.ingestion.loaders.loader import Loader


DATA_FOLDER = 'data'

def ingest_files_data_folder(index: FAISSIndex):
    """Ingests all files in the data folder into the FAISS index and tests chunking."""
    for file in os.listdir(DATA_FOLDER):
        if os.path.isdir(os.path.join(DATA_FOLDER, file)):
            # ignore directories
            continue
        
        loader = Loader(extension=file.split(".")[-1], filepath=os.path.join(DATA_FOLDER, file))
        
        # Extract text, metadata, and chunks
        text = loader.extract_text()
        metadata = loader.extract_metadata()
        chunks = loader.extract_chunks()  # Ensure the method is being called here

        print(f"\nIngesting {file}")
        
        # Test the chunking: Print the first few chunks
        print(f"Extracted Chunks for {file}:")
        for idx, chunk in enumerate(chunks[:5]):  # Print first 5 chunks for review
            print(f"Chunk {idx + 1}: {chunk[:100]}...")  # Print the first 100 characters

        # Optionally, you can ingest the chunks instead of the full text
        # If you prefer to ingest chunks, you can modify the following line
        # index.ingest_text(text=text)  # Ingest full text
        for chunk in chunks:
            index.ingest_text(text=chunk)  # Ingest each chunk separately for testing chunking

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    from src.services.models.embeddings import Embeddings
    
    embeddings = Embeddings()
    index = FAISSIndex(embeddings=embeddings.get_embeddings)    

    # Ingest files and test chunking
    ingest_files_data_folder(index)
    
    # Save the FAISS index after processing
    index.save_index()
