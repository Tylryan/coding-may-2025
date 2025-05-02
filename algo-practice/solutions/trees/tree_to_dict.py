def to_dict(self) -> dict[str, any]:
    return {
            "value": self.value,
            "children": [ child.to_dict() for child in self.children ]
    }