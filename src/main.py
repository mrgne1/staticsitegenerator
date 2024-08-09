from textnode import TextNode
import os
import shutil
import re
import converter

def copy(from_dir, to_dir):
    print(f"copying from {from_dir} to {to_dir}")
    if not os.path.exists(from_dir):
        raise ValueError(f"{from_dir} doesn't exist")
    if os.path.exists(to_dir):
        shutil.rmtree(to_dir)
    os.mkdir(to_dir)

    for file in os.listdir(from_dir):
        from_path, to_path = os.path.join(from_dir, file), os.path.join(to_dir, file)
        if os.path.isdir(from_path):
            copy(from_path, to_path)    
        else:
            shutil.copy(from_path, to_path)


def extract_title(markdown):
    h1re = r"^\s*# (.*)"
    matches = re.findall(h1re, markdown)
    if not matches:
        raise Exception("No header in markdown")
    return matches[0].strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = ""
    with open(from_path) as f:
        markdown = f.read()

    template = ""
    with open(template_path) as f:
        template = f.read()

    content = converter.markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title) \
                   .replace("{{ Content }}", content)

    with open(dest_path, "w") as f:
        f.write(html)
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"generating files for {dir_path_content}")
    if not os.path.exists(dir_path_content):
        raise Exception(f"Directory {dir_path_content} doesn't exist")

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    
    for file in os.listdir(dir_path_content):
        from_path, to_path = os.path.join(dir_path_content, file), os.path.join(dest_dir_path, file)
        if os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, to_path)
        else:
            (path, _) = os.path.splitext(to_path)
            print(f"generating {path}.html")
            generate_page(from_path, template_path, f"{path}.html")

def main():
    copy("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    

if __name__ == "__main__":
    main()