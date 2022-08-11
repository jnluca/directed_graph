from dataclasses import dataclass

from vertex import Vertex


@dataclass
class Edge:
    source: Vertex
    destination: Vertex
