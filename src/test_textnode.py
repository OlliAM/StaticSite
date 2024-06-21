import unittest

from utility import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_url_is_none(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node1, node2)

    def test_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertNotEqual(node1, node2)

    def test_textnode_to_htmlnode(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        result = LeafNode("This is a text node").to_html()
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        result2 = LeafNode("This is a bold text node", "b").to_html()
        node3 = TextNode("This is an italic text node", TextType.ITALIC)
        result3 = LeafNode("This is an italic text node", "i").to_html()
        node4 = TextNode("This is a code text node", TextType.CODE)
        result4 = LeafNode("This is a code text node", "code").to_html()
        node5 = TextNode("This is a link text node", TextType.LINK, "google.com")
        result5 = LeafNode("This is a link text node", "a", {"href": "google.com"}).to_html()
        node6 = TextNode("This is an image node", TextType.IMAGE, "google.com")
        result6 = LeafNode("", "img", {"src": "google.com", "alt": "This is an image node"}).to_html()
        self.assertEqual(text_node_to_html_node(node1).to_html(), result)
        self.assertEqual(text_node_to_html_node(node2).to_html(), result2)
        self.assertEqual(text_node_to_html_node(node3).to_html(), result3)
        self.assertEqual(text_node_to_html_node(node4).to_html(), result4)
        self.assertEqual(text_node_to_html_node(node5).to_html(), result5)
        self.assertEqual(text_node_to_html_node(node6).to_html(), result6)

    def test_split_nodes_delimiter(self):
        node1 = [TextNode("This is a `code` text node", TextType.TEXT)]
        result1 = \
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text node", TextType.TEXT)
            ]
        node2 = [TextNode("This is an *italic* text node", TextType.TEXT)]
        result2 = \
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text node", TextType.TEXT)
            ]
        node3 = [TextNode("This is a **bold** text node", TextType.TEXT)]
        result3 = \
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text node", TextType.TEXT)
            ]
        node4 = [TextNode("This is a text node", TextType.TEXT)]

        self.assertEqual(split_nodes_delimiter(node1, '`', TextType.CODE), result1)
        self.assertEqual(split_nodes_delimiter(node2, '*', TextType.ITALIC), result2)
        self.assertEqual(split_nodes_delimiter(node3, '**', TextType.BOLD), result3)
        self.assertEqual(split_nodes_delimiter(node4, '**', TextType.BOLD), node4)

    def test_no_closing_delimiter(self):
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([TextNode("This is an unfinished `code text node", TextType.TEXT)],
                                  '`', TextType.CODE)
        self.assertEqual(str(context.exception), f"No closing {TextType.CODE} delimiter")

    def test_invalid_delimiter(self):
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([TextNode("This is an invalid delimiter", TextType.TEXT)], '~',
                                  TextType.CODE)
        self.assertEqual(str(context.exception), f"Invalid delimiter ~")

    def test_starting_delimiter(self):
        node1 = [TextNode("`code`", TextType.TEXT)]
        result1 = [TextNode("code", TextType.CODE)]
        node2 = [TextNode("*italic*", TextType.TEXT)]
        result2 = [TextNode("italic", TextType.ITALIC)]
        node3 = [TextNode("**bold**", TextType.TEXT)]
        result3 = [TextNode("bold", TextType.BOLD)]
        self.assertEqual(split_nodes_delimiter(node1, '`', TextType.CODE), result1)
        self.assertEqual(split_nodes_delimiter(node2, '*', TextType.ITALIC), result2)
        self.assertEqual(split_nodes_delimiter(node3, '**', TextType.BOLD), result3)

    def test_extract_images(self):
        test1 = ("This is text with an "
                 "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and "
                 "![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)")
        result1 = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                   (
                       "another",
                       "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        test2 = ("This is text with an "
                 "[image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and "
                 "[another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)")
        result2 = []
        self.assertEqual(extract_markdown_images(test1), result1)
        self.assertEqual(extract_markdown_images(test2), result2)

    def test_extract_links(self):
        test1 = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        result1 = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        test2 = "This is text with a ![link](https://www.example.com) and ![another](https://www.example.com/another)"
        result2 = []
        self.assertEqual(extract_markdown_links(test1), result1)
        self.assertEqual(extract_markdown_links(test2), result2)

    def test_split_images(self):
        node1 = [TextNode(
            "This is text with an "
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and "
            "another"
            " ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextType.TEXT,
        )]
        result1 = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets"
                                              "/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets"
                                                     "/course_assets/3elNhQu.png"
                     ),
        ]
        node2 = [
            TextNode("![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                     TextType.TEXT)]
        result2 = [TextNode("image", TextType.IMAGE,
                            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")]
        node3 = [TextNode("This is just text", TextType.TEXT)]
        node4 = [TextNode(
            "Here's text followed by 2 consecutive images "
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
            "![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextType.TEXT,
        )]
        result4 = [
            TextNode("Here's text followed by 2 consecutive images ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets"
                                              "/course_assets/zjjcJKZ.png"),
            TextNode("second image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets"
                                                     "/course_assets/3elNhQu.png"
                     ),
        ]
        node5 = [TextNode("", TextType.TEXT)]
        node6 = [TextNode("![im@ge!](http://example.com/im@ge!$.png)", TextType.TEXT)]
        result6 = [TextNode("im@ge!", TextType.IMAGE, "http://example.com/im@ge!$.png")]
        node7 = [TextNode("![image1](url1)a![image2](url2)", TextType.TEXT)]
        result7 = [TextNode("image1", TextType.IMAGE, "url1"),
                   TextNode("a", TextType.TEXT),
                   TextNode("image2", TextType.IMAGE, "url2")]
        self.assertEqual(split_nodes_image(node1), result1)
        self.assertEqual(split_nodes_image(node2), result2)
        self.assertEqual(split_nodes_image(node3), node3)
        self.assertEqual(split_nodes_image(node4), result4)
        self.assertEqual(split_nodes_image(node5), [])
        self.assertEqual(split_nodes_image(node6), result6)
        self.assertEqual(split_nodes_image(node7), result7)

    def test_split_links(self):
        node1 = [TextNode(
            "This is text with a "
            "[link](example.com) and "
            "another"
            " [second link](google.com)",
            TextType.TEXT,
        )]
        result1 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "example.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "google.com"
                     ),
        ]
        self.assertEqual(split_nodes_link(node1), result1)

    def test_text_to_textnodes(self):
        node1 = ("This is **text** with an *italic* word and a `code block` and an ![image]("
                 "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a ["
                 "link](https://boot.dev)")
        result1 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE,
                     "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(node1), result1)


if __name__ == "__main__":
    unittest.main()
