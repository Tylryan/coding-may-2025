def btree_cmp(lhs: BinaryNode, rhs: BinaryNode) -> bool:
    # If both sides are None, then it got the end
    # and found no discrepencies.
    if lhs is None and rhs is None:
        return True

    # if one side was none and the other wasn't, then
    # they can't be the same
    if lhs is None or rhs is None:
        return False

    # The actual test.
    if lhs.value != rhs.value:
        return False

    return btree_cmp(lhs.left, rhs.left) and btree_cmp(lhs.right, rhs.right)