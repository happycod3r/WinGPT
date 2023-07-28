import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(CURRENT_PATH, "config")
LOGS_DIR = os.path.join(CURRENT_PATH, "logs")
IMAGES_DIR = os.path.join(CURRENT_PATH, "images")
TMP_DIR = os.path.join(CURRENT_PATH, "tmp")

SYSTEM_LOG_FILE = os.path.join(LOGS_DIR, "system.log")
CHAT_LOG_FILE = os.path.join(LOGS_DIR, "chat.log")
USER_SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.ini")
KEY_CONFIG_FILE = os.path.join(CONFIG_DIR, ".api_key.ini")

SETUP_DONE_FLAG_FILE = os.path.join(CONFIG_DIR, ".setup.flag")
GUI_SHOWN_FLAG_FILE = os.path.join(CONFIG_DIR, ".gui.flag")

TMP_EMBEDDINGS_FILE = os.path.join(TMP_DIR, "embedding.tmp")
TMP_TRANSCRIPT_FILE = os.path.join(TMP_DIR, "transcript.tmp")
TMP_IMAGE_URL_FILE = os.path.join(TMP_DIR, "img_url.tmp")

SETUP_BG_IMAGE = os.path.join(IMAGES_DIR, "openai_dark.png")
GUI_SIDEBAR_LOGO = os.path.join(IMAGES_DIR, "wingtp-alpha-trimmed.png")
