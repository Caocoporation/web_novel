import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def delete_junk_image(origin_avatar_link):
    if os.path.exists(origin_avatar_link):
        os.remove(origin_avatar_link)


 