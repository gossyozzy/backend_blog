import os
from pathlib import Path

from markdown_to_html import *

def extract_title(markdown):
    # Extract the title from the markdown content
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("Title not found in markdown content")



def generate_page(base_path, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path} ...")
    
    markdown_content = ""
    with open(from_path, "r") as f:
        markdown_content = f.read()
    
    template_content = ""
    with open(template_path, "r") as f:
        template_content = f.read()

    html_content = markdown_to_html(markdown_content).to_html()

    title = extract_title(markdown_content)

    final_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content).replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')
    
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, "w") as f:
        f.write(final_content)


def generate_pages_recursive(base_path, dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item)
        if os.path.isdir(item_path):
            # Recursively generate pages for subdirectories
            generate_pages_recursive(base_path, item_path, template_path, dest_item_path)
        elif item.endswith(".md"):
            # Generate page for markdown files
            dest_file_path = Path(dest_item_path).with_suffix(".html")
            generate_page(base_path, item_path, template_path, dest_file_path)