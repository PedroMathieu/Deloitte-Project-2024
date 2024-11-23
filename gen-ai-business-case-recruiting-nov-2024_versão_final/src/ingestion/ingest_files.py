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
        full_text= loader.extract_text()
        print(f"\nIngesting {file}")
        print(full_text)
        index.ingest_text(text=full_text)

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
