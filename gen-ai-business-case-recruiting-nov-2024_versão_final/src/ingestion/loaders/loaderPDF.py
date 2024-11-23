from src.ingestion.loaders.loaderBase import LoaderBase
from pathlib import Path
import fitz  
import pypdf
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
        pdf_file_reader = pypdf.PdfReader(self.filepath)
        doc_info = pdf_file_reader.metadata
        metadata = {  
            'author': doc_info.author,  
            'creator': doc_info.creator,  
            'producer': doc_info.producer,  
            #'subject': doc_info.subject,  
            'title': doc_info.title,  
            #'number_of_pages': len(doc_info.pages)  
        }
        self.metadata=metadata
        
        #return self.metadata if self.all_keys_have_values(metadata=self.metadata) else False
        return self.metadata
    
    def extract_text(self):
        with open(self.filepath, 'rb') as file:
            reader = pypdf.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                text += " " + reader.pages[page_num].extract_text()
        metadata = self.extract_metadata()
        if metadata:
            metadata_text = " ".join([f"{key}: {value}" for key, value in metadata.items() if value])
            text = metadata_text + "\n" + text
        else:
            text = text
       # image_text = self.extract_image_text_from_pdf()
        #text = text + image_text
        return text
    
    def extract_image_text_from_pdf(self):
    # Open the PDF file
        doc = fitz.open(self.filepath)
        
        text_from_images = ""
        
        # Iterate through the pages of the PDF
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Get the list of images on the page
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]  # Image reference
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]  # Get image bytes
                
                # Open the image with PIL (Image object)
                image = Image.open(io.BytesIO(image_bytes))
                
                # Use pytesseract to extract text from the image
                text_from_images += pytesseract.image_to_string(image)
        
        return text_from_images

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

    def all_keys_have_values(self, metadata, value_check=lambda x: x is not None and x != ''):
        return all(value_check(value) for value in metadata.values())
