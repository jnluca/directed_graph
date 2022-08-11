from dataclasses import dataclass


@dataclass
class Vertex:
    label: str

    def __eq__(self, other):
        return self.label == other.label
