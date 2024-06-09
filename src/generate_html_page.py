import os

from pprint import pprint
from block_markdown import markdown_to_blocks, markdown_to_html_node

def extract_title(markdown):
    title = markdown_to_blocks(markdown)
    
    if title == ['']:
        raise ValueError("markdown cannot be an empty string")

    if not title[0].startswith("#"):
        raise ValueError("markdown invalid. make sure the first block in markdown does start with \"# \"")
    
    return title[0].lstrip("# ")


def generate_page(from_path, template_path, dest_path):
    print(f"[INFO] Generating page from {from_path} to {dest_path} using {template_path}")

    article_body = ""
    with open(from_path, 'r') as markdown:
        md = markdown.read()
        title = extract_title(md)
        blocks = markdown_to_html_node(md)
        article_body += blocks.to_html()

        with open(template_path, 'r') as tmpl:
            content = tmpl.read()
            content = content.replace("{{ Title }}", title)
            content = content.replace("{{ Content }}", article_body)

            with open(dest_path, 'w') as new_page:
                # See if destination dir exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Create new page with content
                new_page.write(content)
