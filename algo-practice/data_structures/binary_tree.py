from __future__ import annotations
from random import randint
import json

from collections import deque
from copy import deepcopy

class BinaryNode:
    value: int
    left : BinaryNode
    right: BinaryNode

    def __init__(self, value: int):
        self.value = value
        self.left  = None
        self.right = None

    def __repr__(self):
        return f"Node({self.value})"


    def dfsr(self, target: int) -> BinaryNode:
        if self.value == target:
            return self

        if self.left:
            left = self.left.dfsr(target)
            if left and left.value == target:
                return left

        if self.right:
            right = self.right.dfsr(target)
            if right and right.value == target:
                return right

        return None

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


    def random() -> BinaryNode:
        root = BinaryNode(500)
    
        cache: set[int] = set()
        for i in range(20):
            num = randint(0,1000)
            while num in cache:
                num = randint(0,1000)

            root.insert(num)
            cache.add(num)
        return [list(cache), root ]


    def insert(self, val: int) -> None:
        if val < self.value:
            if self.left is None:
                self.left = BinaryNode(val)
            else:
                self.left.insert(val)
        else:
            if self.right is None:
                self.right = BinaryNode(val)
            else:
                self.right.insert(val)


    def to_dict(self):
        left = "null"
        right = "null"

        if self.left:
            left = self.left.to_dict()
        if self.right:
            right = self.right.to_dict()

        return {
                "value": self.value,
                "left" : left,
                "right": right
        }

    def copy(self) -> BinaryNode:
        node = BinaryNode(deepcopy(self.value))
        if self.left:
            node.left = self.left.copy()
        if self.right:
            node.right = self.right.copy()
        return node

if __name__ == "__main__":

    [cache, tree] = BinaryNode.random()
    num = cache[randint(0, len(cache)-1)]

    dictionary = json.dumps(tree.to_dict(), indent = 2)
    print(dictionary)
    print("FINDING: ", num)

    print("BFSI FOUND: ", tree.bfsi(num))
    print("DFSR FOUND: ", tree.dfsr(num).value)
