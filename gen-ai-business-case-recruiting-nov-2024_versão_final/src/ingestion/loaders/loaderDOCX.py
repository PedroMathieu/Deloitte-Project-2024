from src.ingestion.loaders.loaderBase import LoaderBase
from docx import Document
from docx.shared import Inches
import pytesseract
from PIL import Image
import io

class LoaderDOCX(LoaderBase):

    def __init__(self, filepath: str):
        self.filepath = filepath

    def extract_metadata(self):
        doc = Document(self.filepath)
        metadata = {
            'author': doc.core_properties.author,
            'title': doc.core_properties.title,
            'subject': doc.core_properties.subject,
            'keywords': doc.core_properties.keywords,
            'created': doc.core_properties.created,
        }
        self.metadata = metadata
        return metadata if any(metadata.values()) else False

    def extract_text(self):
        # Extract paragraphs
        doc = Document(self.filepath)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"

        # Extract tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += cell.text + " "

        # Combine with metadata
        metadata = self.extract_metadata()
        if metadata:
            metadata_text = " ".join([f"{key}: {value}" for key, value in metadata.items() if value])
            text = metadata_text + "\n" + text

        # Extract and append image text
        #image_text = self.extract_image_text()
        #return text + "\n" + image_text
        return text

    def extract_image_text(self):
        doc = Document(self.filepath)
        text_from_images = ""
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref.lower():
                try:
                    img_stream = io.BytesIO(rel.target_part._blob)
                    image = Image.open(img_stream)
                    text_from_images += pytesseract.image_to_string(image)
                except Exception as e:
                    print(f"Error processing image: {e}")
        return text_from_images

    def all_keys_have_values(self, metadata, value_check=lambda x: x is not None and x != ''):
        return all(value_check(value) for value in metadata.values())
