import pyzipper
import os
from logger import logger

class ZipManager:
    def __init__(self, zip_path, password=None):
        self.zip_path = zip_path
        self.password = password.encode() if password else None

    def extract_all(self, output_dir):
        try:
            with pyzipper.AESZipFile(self.zip_path, 'r') as zipf:
                if self.password:
                    zipf.pwd = self.password
                zipf.extractall(output_dir)
            logger.info(f"Extracted {self.zip_path} to {output_dir}")
        except Exception as e:
            logger.error(f"Error extracting: {e}")
            raise

    def list_files(self):
        try:
            with pyzipper.AESZipFile(self.zip_path, 'r') as zipf:
                if self.password:
                    zipf.pwd = self.password
                return zipf.namelist()
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            raise

    def add_file(self, file_path, arcname=None):
        try:
            arcname = arcname or os.path.basename(file_path)
            with pyzipper.AESZipFile(self.zip_path, 'a', encryption=pyzipper.WZ_AES) as zipf:
                if self.password:
                    zipf.setpassword(self.password)
                zipf.write(file_path, arcname)
            logger.info(f"Added {file_path} as {arcname}")
        except Exception as e:
            logger.error(f"Error adding file: {e}")
            raise

    def delete_file(self, filename):
        try:
            with pyzipper.AESZipFile(self.zip_path, 'r') as zipf:
                if self.password:
                    zipf.pwd = self.password
                items = {name: zipf.read(name) for name in zipf.namelist() if name != filename}
            with pyzipper.AESZipFile(self.zip_path, 'w', encryption=pyzipper.WZ_AES) as zipf:
                if self.password:
                    zipf.setpassword(self.password)
                for name, data in items.items():
                    zipf.writestr(name, data)
            logger.info(f"Deleted {filename} from archive")
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            raise

    def search_file(self, keyword):
        try:
            files = self.list_files()
            matches = [f for f in files if keyword.lower() in f.lower()]
            logger.info(f"Search for {keyword}: {matches}")
            return matches
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            raise
