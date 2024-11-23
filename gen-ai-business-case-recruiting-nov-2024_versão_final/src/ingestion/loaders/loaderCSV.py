import csv
import os
from src.ingestion.loaders.loaderBase import LoaderBase

class LoaderCSV(LoaderBase):

    def __init__(self, filepath: str):
        self.filepath = filepath

    def extract_metadata(self):
        """
        Extracts metadata from the CSV file such as filename, number of rows, columns, and headers.
        Returns:
            dict: Metadata including filename, number of rows, columns, and headers.
        """
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
            'headers': headers if headers else "No headers"
        }
        
        self.metadata = metadata
        return metadata

    def extract_text(self):
        """
        Extracts the plain text representation of the CSV file's data.
        Combines metadata and plain text content (without any delimiters).
        Returns:
            str: Combined metadata and plain text content of the CSV file.
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        # Extract metadata
        metadata = self.extract_metadata()
        metadata_text = "\n".join([f"{key}: {value}" for key, value in metadata.items() if value])

        # Extract text from CSV
        text = ""
        with open(self.filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, None)  # Read the header row if it exists
            if headers:
                text += '\n'.join(headers) + '\n'  # Append headers without delimiter
            
            for row in reader:
                text += ' '.join(row) + '\n'  # Join row elements with spaces, no delimiter
        
        # Combine metadata and plain text content
        return metadata_text + text
