from copy import deepcopy

def btree_deepcopy(tree: BinaryNode) -> BinaryNode:
    if tree is None:
        return None

    node = BinaryNode(deepcopy(tree.value))
    node.left = btree_deepcopy(tree.left)
    node.right = btree_deepcopy(tree.right)
    return node