import os
import shutil

from static_files import copy_static
from generate_html_page import generate_page

def main():
    source = "static"
    destination = "public"

    copy_static(source, destination)
    generate_page("content/index.md", "templates/template.html", "public/index.html")

if __name__ == "__main__":
    main()