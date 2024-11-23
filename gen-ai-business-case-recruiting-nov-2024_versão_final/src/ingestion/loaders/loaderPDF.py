from src.ingestion.loaders.loaderBase import LoaderBase
from pathlib import Path
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import io
import os
import tempfile

class LoaderPDF(LoaderBase):

    def __init__(self, filepath:str):
        self.filepath=filepath

    def extract_metadata(self):
        pdf_file_reader = PyPDF2.PdfReader(self.filepath)
        doc_info = pdf_file_reader.metadata
        metadata = {  
            'author': doc_info.author,  
            'creator': doc_info.creator,  
            'producer': doc_info.producer,  
            'subject': doc_info.subject,  
            'title': doc_info.title,  
            #'number_of_pages': len(doc_info.pages)  
        }

        self.metadata=metadata
        
        return self.metadata if self.all_keys_have_values(metadata=self.metadata) else False
    
    def extract_text(self):
        with open(self.filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                text += " " + reader.pages[page_num].extract_text()
        return text
    
    def extract_image_text(self, page_num: int):
        """Extract text from images on a specific page using OCR."""
        images = convert_from_path(self.filepath, first_page=page_num + 1, last_page=page_num + 1)
        if not images:
            return ""
        
        text = ""
        for image in images:
            # Use pytesseract to extract text from the image
            text += pytesseract.image_to_string(image)
        
        return text

    def extract_chunks(self):
        """Chunk the extracted text into paragraphs."""
        text = self.extract_text()
        
        if not text:
            return []
        
        paragraphs = text.split("\n\n")
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        return paragraphs

    def extract_image_chunks(self):
        """Extract text from images in the PDF and chunk them into paragraphs."""
        num_pages = len(PyPDF2.PdfReader(self.filepath).pages)
        image_chunks = []
        
        for page_num in range(num_pages):
            text_from_images = self.extract_image_text(page_num)
            if text_from_images:
                image_chunks.extend(text_from_images.split("\n\n"))
        
        return [chunk.strip() for chunk in image_chunks if chunk.strip()]

    def all_keys_have_values(self, metadata, value_check=lambda x: x is not None and x != ''):
        return all(value_check(value) for value in metadata.values())
