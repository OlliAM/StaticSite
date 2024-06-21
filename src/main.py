from textnode import TextNode
from utility import *
from blocks import *


def main():
    copy_dir_to_new_dir(r"static", r"public")
    generate_pages_recursive(r"content",
                             r"template.html",
                             r"public")


if __name__ == "__main__":
    main()
