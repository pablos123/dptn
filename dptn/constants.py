import os
from pathlib import Path

DPT_URL = "https://tracker.debian.org/"
NEWS_URL = "https://tracker.debian.org/pkg/{}/news/?page={}"
DPTN_DIR_PATH = Path(os.getenv("HOME")) / ".dptn"
