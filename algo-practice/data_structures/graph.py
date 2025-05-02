from __future__ import annotations

class GraphNode:
    value: int
    parents: list[GraphNode]
    children: list[GraphNode]


    def __init__(self, value: int, parents = None, children = None):
        self.value    = value
        self.parents  =  parents or []
        self.children = children or []

    def __repr__(self) -> str:
        return str(self.value)

    def add_child(self, value: int) -> GraphNode:
        gn = GraphNode(value)
        self.children.append(gn)
        return gn

    def add_children(self, values: list[int]) -> list[GraphNode]:
        gns: list[GraphNode] = []
        for v in values:
            gn = GraphNode(v)
            self.add_child(gn)
            gns.append(gn)
        return gns

    def add_parents(self, values: list[int]) -> list[GraphNode]:
        gns: list[GraphNode] = []
        for v in values:
            gn = GraphNode(v)
            self.add_parent(v)
            gns.append(gn)
        return gns

    def add_parent(self, value: int) -> GraphNode:
        gn = GraphNode(value)
        self.parents.append(gn)
        return gn

    def print(self):
        d = self.as_dict()
        import json
        from pprint import pprint
        pprint(d, indent = 2, sort_dicts=False)


    def default(self, level = 2) -> GraphNode:
        """Creates a graph with 5 parents and 5 children.
        Each parent and each child has one level of children."""

        from random import randint
        things: list[GraphNode] = [self]

        for t in things:
            c = t.add_child(randint(0, 1000))
            p = t.add_parent(randint(0,1000))

            if level > 0:
                things = [c.default(level -1), p.default(level - 1)]

        return self
            



    def as_dict(self):
        return {
            "value": self.value,
            "parents": [parent.as_dict() for parent in self.parents],
            "children": [ child.as_dict() for child in self.children]
        }

if __name__ == "__main__":
    from pprint import pprint

    graph = GraphNode(10)
    # c1: list[GraphNode] = graph.add_children([1,2,3,4])
    # p1: list[GraphNode] = graph.add_parents([5,6,7,8])
    #graph.print()

    g = graph.default(10)
    g.print()
