import os
import re
import tkinter as tk
from tkinter import filedialog


def extract_link(filepath):
    """find the first link in aspx file"""
    link = None
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            # 找第一個 url
            match = re.search(r'href=["\'](.*?)["\']', content)
            if match:
                link = match.group(1)
    except Exception as e:
        print(f"error reading {filepath}: {e}")
    return link

def create_url_file(aspx_filepath, url):
    """create url file"""
    if url:
        file_name = os.path.splitext(os.path.basename(aspx_filepath))[0]
        
        script_folder_path = os.path.dirname(os.path.abspath(__file__))
        url_file_path = os.path.join(script_folder_path, f"{file_name}.url")

        try:
            # 生成 .url
            with open(url_file_path, 'w', encoding='utf-8') as file:
                file.write(f"[InternetShortcut]\nURL={url}\n")
            print(f".url file created: {url_file_path}")
        except Exception as e:
            print(f"error: {e}")
    else:
        print(f"no link found, no url extracted。")

def select_aspx_file():
    """use selector"""
    root = tk.Tk()
    root.withdraw()
    aspx_filepath = filedialog.askopenfilename(filetypes=[("ASPX files", "*.aspx")])

    if aspx_filepath:
        print(f"select file: {aspx_filepath}")
        url = extract_link(aspx_filepath)
        if url:
            create_url_file(aspx_filepath, url)
        else:
            print("no link found")
    else:
        print("no file selected")

# execute first process in pipe
select_aspx_file()
