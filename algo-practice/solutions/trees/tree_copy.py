def btree_copy(tree: BinaryNode) -> BinaryNode:
    if tree is None:
        return None

    new_node = BinaryNode(tree.value)
    new_node.left = tree.left
    new_node.right = tree.right
    return new_node