from typing import List, Dict

from edge import Edge
from vertex import Vertex


class DirectedGraph:
    # We put ourselves in the case of a multigraph,
    # in which we can have several edges between 2 vertices

    def __init__(self, vertices_list: List[Vertex], edges_list: List[Edge]):
        self.vertices: List[Vertex] = list(set(vertices_list))
        self.edges: List[Edge] = edges_list

    def compute_number_of_edges(self) -> int:
        return len(self.edges)

    def compute_number_of_vertices(self) -> int:
        return len(self.vertices)

    def compute_in_degrees_per_vertex(self) -> Dict[Vertex, int]:
        in_degrees = dict()
        for vertex in self.vertices:
            in_degrees[vertex] = 0
        for edge in self.edges:
            in_degrees[edge.destination] += 1
        return in_degrees

    def compute_out_degrees_per_vertex(self) -> Dict[Vertex, int]:
        out_degrees = dict()
        for vertex in self.vertices:
            out_degrees[vertex] = 0
        for edge in self.edges:
            out_degrees[edge.source] += 1
        return out_degrees


