def bfsi(self, target: int) -> BinaryNode:
    queue: list[BinaryNode] = [self]

    while queue:
        node = queue[0]
        queue = queue[1:]

        if node is None:
            continue

        if node.value == target:
            return node

        queue += [node.left, node.right]

    return None