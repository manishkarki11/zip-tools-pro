import logging
import os

# Setup logs folder
os.makedirs("logs", exist_ok=True)

# Setup Logger
logger = logging.getLogger("zip_tool")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("logs/zip_tool.log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)
