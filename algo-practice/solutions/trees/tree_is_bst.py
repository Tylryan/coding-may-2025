# Given a binary tree, check if it is a Binary Search Tree.
# The value of a given node should be greater than the left node's value
# and less than the right node's value.

def is_bst(tree: BinaryNode) -> bool:
    def __is_bst(node, min_val = float("-inf"), max_val = float("inf")):
        if node is None:
            return True
        if not(min_val < node.value < max_val):
            return False
        return (
            __is_bst(node.left, min_val, node.value) and
            __is_bst(node.right, node.value, max_val)
        )

    return __is_bst(tree)