from __future__ import annotations
from pprint import pprint


class TreeNode:
    value: object
    children: list[TreeNode]
    def __init__(self, value: object):
        self.value = value
        self.children = []

    def __repr__(self):
        return f"{self.value}"

    def add_child(self, child: TreeNode) -> None:
        self.children.append(child)

    def from_dict(data: dict[str, object]) -> TreeNode:
        node = TreeNode(data["value"])
        for child_data in data.get("children", []):
            child_node = TreeNode.from_dict(child_data)
            node.add_child(child_node)
        return node

    def to_dict(self) -> dict[str, any]:
        return {
                "value": self.value,
                "children": [ child.to_dict() for child in self.children ]
        }

    def default() -> TreeNode:
        """Creates """
        root = TreeNode(1)
        child_one = TreeNode(2)
        child_two = TreeNode(3)
        root.add_child(child_one)
        root.add_child(child_two)

        grand_child = TreeNode(4)
        child_one.add_child(grand_child)

        return root

    def print(self, indent: str = "-") -> None:
        print(indent + " " + str(self.value))

        for child in self.children:
            child.print(indent + "-")

# Just an example of how to do it as a function instead
# of a method.
def print_tree(node: TreeNode, indent: str = "-") -> None:
    print(indent + " " + str(node.value))
    for child in node.children:
        print_tree(child, indent + "-")


if __name__ == "__main__":
    import json
    tree: TreeNode = TreeNode.default()
    tree.print()
    print(json.dumps(tree.to_dict(), indent = 2))


    json_str = '{"value":"root","children": [{"value": "child_one", "children": []}]}'
    hmap = json.loads(json_str)
    new_tree = TreeNode.from_dict(hmap)
    new_tree.print()

