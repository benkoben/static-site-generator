from static_files import copy_static
from generate_html_page import generate_pages_recursive

def main():
    source = "static"
    destination = "public"

    copy_static(source, destination)
    generate_pages_recursive("content", "templates/template.html", "public")

if __name__ == "__main__":
    main()