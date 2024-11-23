from src.ingestion.loaders.loaderBase import LoaderBase
from docx import Document


class LoaderDOCX(LoaderBase):

    def __init__(self, filepath: str):
        self.filepath = filepath

    def extract_metadata(self):
        # Load the .docx file
        doc = Document(self.filepath)
        
        # Extract metadata from core properties
        metadata = {
            'author': doc.core_properties.author,
            'title': doc.core_properties.title,
            'subject': doc.core_properties.subject,
            'keywords': doc.core_properties.keywords,
            'created': doc.core_properties.created,
        }
        
        self.metadata = metadata
        
        # Check if all metadata values are available (non-empty)
        return self.metadata if self.all_keys_have_values(metadata=self.metadata) else False
    
    def extract_text(self):
        # Load the .docx file
        doc = Document(self.filepath)
        
        # Extract all text from paragraphs and return as a single string
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"  # Adding newlines between paragraphs
        
        return text

    def extract_chunks(self):
        raise NotImplementedError("Chunk extraction not implemented for DOCX files.")

    def all_keys_have_values(self, metadata, value_check=lambda x: x is not None and x != ''):
        # Helper method to ensure all metadata values are non-empty
        return all(value_check(value) for value in metadata.values())
