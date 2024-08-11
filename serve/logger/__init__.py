import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=os.path.join(os.path.dirname(__file__), "life-bookshelf-ai.log"),
    filemode="a",
)

# 특정 로거 'life-bookshelf-ai' 설정 (DEBUG 레벨)
logger = logging.getLogger("life-bookshelf-ai")
logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))
