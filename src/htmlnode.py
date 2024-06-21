class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        for k, v in self.props.items():
            result += f' {k}="{v}"'
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode value cannot be None")
        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return self.value


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag cannot be None")
        if not self.children:
            raise ValueError("ParentNode has no children")

        html_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_string += child.to_html()
        return f"{html_string}</{self.tag}>"
