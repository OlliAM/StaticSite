import textwrap
import unittest

from utility import *
from blocks import *


def normalize_html(html):
    # Remove leading/trailing whitespace newlines
    html = html.strip()
    # Remove spaces between tags
    html = re.sub(r'>\s+<', '><', html)
    # Remove multiple spaces within tags' content
    html = re.sub(r'\s+', ' ', html)
    return html


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown1 = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""

        result1 = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]
        self.assertEqual(markdown_to_blocks(markdown1), result1)

    def test_empty_input_string(self):
        markdown = ""
        result = []
        self.assertEqual(markdown_to_blocks(markdown), result)

    def test_whitespace_blocks(self):
        markdown = textwrap.dedent("""\
                   First block

                   Second block


                   Third block
               """)
        result = [
            "First block",
            "Second block",
            "Third block"
        ]
        self.assertEqual(markdown_to_blocks(markdown), result)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a simple paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("`` Not a code block"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("*Not an unordered list item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1 . Not an ordered list item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(
            "This is a multi-line paragraph.\nStill going on the second line.\nYet more on the third line."),
            BlockType.PARAGRAPH)

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode block\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("`` Not a code block"), BlockType.PARAGRAPH)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Another line of the quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> This is a quote\n> Another line of the quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Yet another line of the quote\n> And one more"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Another list item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("*Not an unordered list item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-Not an unordered list item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("* List item\n* Another list item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("* List item\n- Mixed list item"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1 . Not an ordered list item"),
                         BlockType.PARAGRAPH)  # Incorrect ordered list
        self.assertEqual(block_to_block_type("2 - Not an ordered list item"),
                         BlockType.PARAGRAPH)  # Incorrect ordered list
        self.assertEqual(block_to_block_type("1.1 Not an ordered list item"),
                         BlockType.PARAGRAPH)  # Incorrect ordered list
        self.assertEqual(block_to_block_type("1. First item\n2. Second item\n3. Third item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. First item\n2. Second item\n4. Incorrect item"),
                         BlockType.PARAGRAPH)  # Incorrect ordered list

    def test_quote_block_to_html_node(self):
        block1 = ">This is a quote block\n>And it's looking damn fine"
        result1 = "<blockquote>This is a quote block\nAnd it's looking damn fine</blockquote>"
        block2 = "> This is a quote on a single line"
        result2 = "<blockquote>This is a quote on a single line</blockquote>"
        block3 = "> This is a quote with a following empty line\n> "
        result3 = "<blockquote>This is a quote with a following empty line</blockquote>"
        self.assertEqual(quote_block_to_htmlnode(block1).to_html(), result1)
        self.assertEqual(quote_block_to_htmlnode(block2).to_html(), result2)
        self.assertEqual(quote_block_to_htmlnode(block3).to_html(), result3)

    def test_heading_block_to_html_node(self):
        block1 = "# This is h1"
        result1 = "<h1>This is h1</h1>"
        block2 = "## This is h2"
        result2 = "<h2>This is h2</h2>"
        block3 = "### This is h3"
        result3 = "<h3>This is h3</h3>"
        block4 = "#### This is h4"
        result4 = "<h4>This is h4</h4>"
        block5 = "##### This is h5"
        result5 = "<h5>This is h5</h5>"
        block6 = "###### This is h6"
        result6 = "<h6>This is h6</h6>"
        block7 = "####### This is h7"  #Not possible, but worth testing
        result7 = "<h6>This is h7</h6>"
        self.assertEqual(heading_block_to_htmlnode(block1).to_html(), result1)
        self.assertEqual(heading_block_to_htmlnode(block2).to_html(), result2)
        self.assertEqual(heading_block_to_htmlnode(block3).to_html(), result3)
        self.assertEqual(heading_block_to_htmlnode(block4).to_html(), result4)
        self.assertEqual(heading_block_to_htmlnode(block5).to_html(), result5)
        self.assertEqual(heading_block_to_htmlnode(block6).to_html(), result6)
        self.assertEqual(heading_block_to_htmlnode(block7).to_html(), result7)

    def test_code_block_to_html_node(self):
        block1 = "```This is a code block\nWhich is full of lots of interesting\ncode```"
        result1 = "<pre><code>This is a code block\nWhich is full of lots of interesting\ncode</code></pre>"
        self.assertEqual(code_block_to_htmlnode(block1).to_html(), result1)

    def test_unordered_list_block_to_html_node(self):
        block1 = "* This is a single item list"
        result1 = "<ul><li>This is a single item list</li></ul>"
        block2 = "* This is\n- A multi\n* Item list"
        result2 = "<ul><li>This is</li><li>A multi</li><li>Item list</li></ul>"
        self.assertEqual(unordered_list_block_to_htmlnode(block1).to_html(), result1)
        self.assertEqual(unordered_list_block_to_htmlnode(block2).to_html(), result2)

    def test_ordered_list_block_to_html_node(self):
        block1 = "1. This is a single item list"
        result1 = "<ol><li>This is a single item list</li></ol>"
        block2 = "1. This is\n2. A multi\n3. Item list"
        result2 = "<ol><li>This is</li><li>A multi</li><li>Item list</li></ol>"
        self.assertEqual(ordered_list_block_to_htmlnode(block1).to_html(), result1)
        self.assertEqual(ordered_list_block_to_htmlnode(block2).to_html(), result2)

    def test_paragraph_block_to_html_node(self):
        block1 = "This is literally just a paragraph"
        result1 = "<p>This is literally just a paragraph</p>"
        self.assertEqual(paragraph_block_to_htmlnode(block1).to_html(), result1)

    def test_markdown_to_html(self):
        markdown = textwrap.dedent("""
        # Heading 1

        ## Heading 2

        > This is a blockquote

        * List item 1
        - List item 2

        1. Ordered item 1
        2. Ordered item 2

        ```Code block```


        A paragraph of text.
        """)
        expected_html = textwrap.dedent("""
        <div>
        <h1>Heading 1</h1>
        <h2>Heading 2</h2>
        <blockquote>This is a blockquote</blockquote>
        <ul>
            <li>List item 1</li>
            <li>List item 2</li>
        </ul>
        <ol>
        <li>Ordered item 1</li>
        <li>Ordered item 2</li>
        </ol>
        <pre><code>Code block</code></pre>
        <p>A paragraph of text.</p>
        </div>
        """)
        test1 = """# The Unparalleled Majesty of "The Lord of the Rings"

[Back Home](/)

![LOTR image artistmonkeys](/images/rivendell.png)

> "I cordially dislike allegory in all its manifestations, and always have done so since I grew old and wary enough to detect its presence.
> I much prefer history, true or feigned, with its varied applicability to the thought and experience of readers.
> I think that many confuse 'applicability' with 'allegory'; but the one resides in the freedom of the reader, and the other in the purposed domination of the author."
"""
        result1 = """<h1 id="the-unparalleled-majesty-of-the-lord-of-the-rings-">The Unparalleled Majesty of &quot;The Lord of the Rings&quot;</h1>
<p><a href="/">Back Home</a></p>
<p><img src="/images/rivendell.png" alt="LOTR image artistmonkeys"></p>
<blockquote>
<p>&quot;I cordially dislike allegory in all its manifestations, and always have done so since I grew old and wary enough to detect its presence.
I much prefer history, true or feigned, with its varied applicability to the thought and experience of readers.
I think that many confuse &#39;applicability&#39; with &#39;allegory&#39;; but the one resides in the freedom of the reader, and the other in the purposed domination of the author.&quot;</p>
</blockquote>
"""
        self.assertEqual(normalize_html(markdown_to_html_node(markdown).to_html()), normalize_html(expected_html))
        self.assertEqual(markdown_to_html_node(test1).to_html(), result1)

if __name__ == "__main__":
    unittest.main()
