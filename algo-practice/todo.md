# Trees
## Binary Tree
1. Depth first search
2. Breadth first search (Level Order Traversal).
3. In Order Traversal

1. Preorder
    - + 3 * 4 5
2. Postorder
3. In order



## Tree
1. Depth first search
2. Breadth first search
3. In Order Traversal

## Heaps
1. Min-Heap
2. Max-Heap

## Questions
1. What are n example use cases for DFS/BFS/etc?


## Tries

## Applications
1. Spell Checker


## Modifications
- Add Node
- Remove Node
- Insert Node
- Find Node

## Other Interesting Ideas
1. Copy A Tree: Tree -> Tree
2. Compare Trees: (Tree, Tree) -> bool
2. Reverse A Tree:  Tree -> Tree
3. Tree to list: Tree -> List
4. Sum first/last n levels: Tree -> Int
5. Sum levels between k1 and k2: Tree -> Int
    - If there were 5 levels, sum levels 3 and 4.

# Chat Gippity Questions
1. Binary Tree Traversals (Preorder, Inorder, Postorder)  
Difficulty: Easy → Medium  
What it tests: Recursion, basic understanding of tree structure.  
Prompt:  
    Given the root of a binary tree, return the preorder/inorder/postorder traversal of its nodes' values.
📌 Variants: Ask for recursive first, then iterative (to test stack-based reasoning).

2. Validate a Binary Search Tree (BST)
Difficulty: Medium
What it tests: Understanding of BST properties, recursive range constraints
Prompt:
    Write a function to determine if a binary tree is a valid binary search tree.
📌 Follow-up: Ask what would change if duplicate values are allowed, or ask for iterative solution.

3. Lowest Common Ancestor (LCA) in a Binary Tree
Difficulty: Medium → Hard
What it tests: Tree traversal, recursive reasoning, managing return values
Prompt:
    Given a binary tree and two nodes, return their lowest common ancestor (LCA).
    All node values are unique, and both nodes are guaranteed to exist in the tree.
📌 Follow-up: How would this change if it were a BST?

4. Serialize and Deserialize a Binary Tree
Difficulty: Medium → Hard
What it tests: Traversal, tree reconstruction, dealing with nulls
Prompt:
    Design a method to serialize a binary tree into a string and deserialize it back into the original tree.
📌 Use preorder or level-order. Bonus: Implement both approaches and compare efficiency.

5. Diameter of a Binary Tree
Difficulty: Medium
What it tests: Tree depth computation, recursive post-order logic, global tracking
Prompt:
    Given the root of a binary tree, return the length of the longest path between any two nodes in the tree.
📌 Tricky part: Path may not pass through the root. Look for candidates who compute height and diameter simultaneously.

6. 🧠 Advanced Bonus – Build Tree from Traversals
Prompt:
    Given preorder and inorder traversal lists of a binary tree, reconstruct the original tree.
What it tests:
Deep understanding of traversal order and recursive tree construction.

7. Constant Folding Optimization
Difficulty: Medium → Hard
What it tests: Tree transformation, compiler optimization concepts
Prompt:
    Given an AST, perform constant folding by simplifying any subtree that consists entirely of constant literals.

📌 Example: (2 + (3 * 4)) → (2 + 12) → 14
📌 Follow-up: How would you avoid simplifying nodes that contain variables?

8. Convert an AST Back to Source Code (Pretty-Printing)
Difficulty: Medium
What it tests: Tree traversal, string construction, formatting logic
Prompt:
    Given an AST representing a subset of a programming language (e.g., arithmetic or a toy imperative language), reconstruct the source code string with proper parentheses and formatting.
📌 Tests: Understanding of precedence, associativity, and code generation.

# Notes
- Preorder/postorder/inorder traversals are ALL Depth First.
