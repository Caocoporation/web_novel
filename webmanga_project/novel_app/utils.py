import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def delete_junk_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)
    
def create_directory(file_name, directory=None):

    create_dir = os.path.join(BASE_DIR, directory, file_name)
      
    if not os.path.exists(create_dir):
        os.makedirs(create_dir)

def resize_image(img, saving_path, size):
    img.thumbnail(size)
    img.save(saving_path) 

def title_convertor(title):
    rename = "_".join(title.split())
    return rename