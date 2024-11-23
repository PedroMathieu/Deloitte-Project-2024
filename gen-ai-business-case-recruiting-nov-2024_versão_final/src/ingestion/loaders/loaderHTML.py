import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
import requests
import os
import html2text
from src.ingestion.loaders.loaderBase import LoaderBase


class LoaderHTML(LoaderBase):
    
    def __init__(self, filepath: str):
        self.filepath = filepath

    def extract_metadata(self):
        """
        Extracts basic metadata from the HTML file, such as title, description, and author.
        Returns:
            dict: A dictionary containing metadata, or False if no metadata is found.
        """
        with open(self.filepath, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            metadata = {
                'title': soup.title.string if soup.title else None,
                'description': (soup.find('meta', attrs={'name': 'description'}) or {}).get('content'),
                'author': (soup.find('meta', attrs={'name': 'author'}) or {}).get('content')
            }
            self.metadata = metadata
            return metadata if any(metadata.values()) else False

    def extract_text(self):
        """
        Extracts plain text from the HTML file using html2text and appends image text extracted via OCR.
        Returns:
            str: The extracted plain text.
        """
        with open(self.filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()
            text_converter = html2text.HTML2Text()
            text_converter.ignore_links = True  # Optional: Skip rendering links
            
            text = text_converter.handle(html_content)
        metadata = self.extract_metadata()
        if metadata:
            metadata_text = " ".join([f"{key}: {value}" for key, value in metadata.items() if value])
            text = metadata_text + "\n" + text
        
        # Append image OCR text
        #image_text = self.extract_image_text()
        #text = text + image_text
        return text

    def extract_image_text(self):
        """
        Finds images in the HTML and extracts text from them using OCR.
        Returns:
            str: A concatenated string of text extracted from all images.
        """
        with open(self.filepath, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
        
        image_text = ""
        for img_tag in soup.find_all('img'):
            img_src = img_tag.get('src')
            if not img_src:
                continue
            
            # Handle local or remote images
            if img_src.startswith('http'):
                # Remote image - download it
                response = requests.get(img_src, stream=True)
                if response.status_code == 200:
                    img = Image.open(response.raw)
                    image_text += "\n" + pytesseract.image_to_string(img)
            else:
                # Local image - load it from disk
                img_path = os.path.join(os.path.dirname(self.filepath), img_src)
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    image_text += "\n" + pytesseract.image_to_string(img)

        return image_text

    def all_keys_have_values(self, metadata, value_check=lambda x: x is not None and x != ''):
        """
        Helper method to check if all keys in the metadata dictionary have valid values.
        """
        return all(value_check(value) for value in metadata.values())
