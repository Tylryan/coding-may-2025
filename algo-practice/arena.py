from data_structures import *
from pprint import pprint
from copy import deepcopy


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


def main():
    [ cache, btree ] = BinaryNode.random()
    cp: BinaryNode = btree.copy()
    cp.value = 1000
    print(cp.value < cp.right.value)

    print("IS_BST: ", is_bst(cp))


if __name__ == "__main__":
    main()



