import os
import shutil
import sys
from generate_page import generate_pages_recursive

from copystatic import copy_files_recursive


dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "content"
template_path = "./template.html"


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Deleting docs directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive(basepath, dir_path_content, template_path, dir_path_public)

main()