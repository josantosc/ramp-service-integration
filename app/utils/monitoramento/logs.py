import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_thread_access(chat_id, action):
    logger.info(f"Action {action} performed on thread for chat_id {chat_id}")
