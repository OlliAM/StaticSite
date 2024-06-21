import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("hi", "hi again", [], {})
        node2 = HTMLNode("hi", "hi again", [], {})
        self.assertEqual(node1.tag, node2.tag)
        self.assertEqual(node1.value, node2.value)
        self.assertEqual(node1.children, node2.children)
        self.assertEqual(node1.props, node2.props)

    def test_props_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node1 = HTMLNode(None, None, None, props)
        result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node1.props_to_html(), result)

    def test_leafnode_eq(self):
        node1 = LeafNode("hi again", "hi", {"key": "value"})
        node2 = LeafNode("hi again", "hi", {"key": "value"})
        self.assertEqual(node1.tag, node2.tag)
        self.assertEqual(node1.value, node2.value)
        self.assertEqual(node1.props, node2.props)

    def test_leaf_test_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node1 = LeafNode("This is a paragraph of text.", "p", None)
        result1 = '<p>This is a paragraph of text.</p>'
        node2 = LeafNode("Click me!", "a", {"href": "https://www.google.com"})
        result2 = '<a href="https://www.google.com">Click me!</a>'
        node3 = LeafNode("This is just a string", None, None)
        result3 = "This is just a string"
        node4 = LeafNode("", "div", {"src": "image.jpg", "alt": "An image", "width": "500"})
        result4 = '<div src="image.jpg" alt="An image" width="500"></div>'
        self.assertEqual(node1.to_html(), result1)
        self.assertEqual(node2.to_html(), result2)
        self.assertEqual(node3.to_html(), result3)
        self.assertEqual(node4.to_html(), result4)

    def test_parent_test_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node1 = ParentNode(
            "p",
            [
                LeafNode("Bold text", "b", None),
                LeafNode("Normal text", None),
                LeafNode("italic text", "i"),
                LeafNode("Normal text", None),
            ])
        result1 = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node1.to_html(), result1)

    def test_no_tag_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(None, [LeafNode("Bold text", "b")])
            node.to_html()
        self.assertEqual(str(context.exception), "Tag cannot be None")

    def test_no_children_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode("p", [])
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode has no children")

    def test_recursion_on_parentnode(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode("Bold text", "b"),
                ParentNode(
                    "a",
                    [
                        LeafNode("Nested bold text", "b"),
                        LeafNode("Nested italic text", "i"),
                        LeafNode("Nested normal text", None),
                    ]),
                LeafNode("italic text", "i"),
                LeafNode("Normal text", None),
            ])
        result1 = ('<p><b>Bold text</b><a><b>Nested bold text</b><i>Nested italic text</i>Nested normal '
                   'text</a><i>italic text</i>Normal text</p>')
        self.assertEqual(node1.to_html(), result1)


if __name__ == "__main__":
    unittest.main()
