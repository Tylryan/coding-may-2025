def from_dict(data: dict[str, object]) -> TreeNode:
    node = TreeNode(data["value"])
    for child_data in data.get("children", []):
        child_node = TreeNode.from_dict(child_data)
        node.add_child(child_node)
    return node