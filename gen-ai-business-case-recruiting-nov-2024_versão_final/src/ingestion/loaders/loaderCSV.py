import csv
import os
from src.ingestion.loaders.loaderBase import LoaderBase

class LoaderCSV(LoaderBase):

    def __init__(self, filepath: str):
        self.filepath = filepath

    def extract_metadata(self):
        """Extracts metadata from the CSV file like number of rows, columns, and headers."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        with open(self.filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, None)  # Read the first row (headers)
            rows = list(reader)  # Read all remaining rows
            
        metadata = {
            'filename': os.path.basename(self.filepath),
            'number_of_rows': len(rows),
            'number_of_columns': len(headers) if headers else 0,
            'headers': headers
        }
        
        return metadata
    
    def extract_text(self):
        """Extracts all text from the CSV file."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        text = ""
        with open(self.filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, None)  # Skip the header row if it exists
            
            for row in reader:
                text += ' '.join(row) + '\n'
        
        return text
