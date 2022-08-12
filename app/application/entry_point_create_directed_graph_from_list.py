import os
from typing import List, Tuple, Dict

from click import command, option

from app.config.logging_config import set_logging_config
from app.directed_graph import DirectedGraph


@command()
@option('--vertices-list', help='List of vertices', type=str, multiple=True, default=['a', 'b', 'c', 'c', 'd', 'e'])
@option('--edges-list', help='List of edges', type=(str, str), multiple=True,
        default=[('a', 'b'), ('a', 'b'), ('d', 'c'), ('b', 'd'), ('a', 'd'), ('c', 'a'),
                 ('b', 'b')])
def build_graph_from_lists(vertices_list: List[str], edges_list: List[Tuple[str, str]]) -> None:
    directed_graph: DirectedGraph = DirectedGraph()
    directed_graph.build_graph_from_vertices_and_edges(vertices_list=vertices_list, edges_list=edges_list)

    vertices_number: int = directed_graph.compute_number_of_vertices()
    edges_number: int = directed_graph.compute_number_of_edges()

    in_degrees: Dict[str, int] = directed_graph.compute_in_degrees_per_vertex()
    out_degrees: Dict[str, int] = directed_graph.compute_out_degrees_per_vertex()

    print("Summary of the graph you entered: ")
    print(f'# Number of vertices is {vertices_number}')
    print(f'# Number of edges is {edges_number}')
    print(f'# in degrees are {in_degrees}')
    print(f'# out degrees are {out_degrees}')

    directed_graph.serialize_graph(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp'))


if __name__ == '__main__':
    set_logging_config()
    build_graph_from_lists()
