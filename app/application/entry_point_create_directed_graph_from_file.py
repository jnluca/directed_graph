import os
from typing import Dict

from click import command, option, Path

from app.config.logging_config import set_logging_config
from app.directed_graph import DirectedGraph


@command()
@option('--filepath', help='Path of the serialized graph', type=Path(),
        default=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp', 'graph.pickle'))
def build_graph_from_pickle_file(filepath: str) -> None:
    directed_graph: DirectedGraph = DirectedGraph()
    directed_graph.build_graph_from_pickle_file(pickle_filepath=filepath)

    vertices_number: int = directed_graph.compute_number_of_vertices()
    edges_number: int = directed_graph.compute_number_of_edges()

    in_degrees: Dict[str, int] = directed_graph.compute_in_degrees_per_vertex()
    out_degrees: Dict[str, int] = directed_graph.compute_out_degrees_per_vertex()

    print("Summary of the graph you entered: ")
    print(f'# Number of vertices is {vertices_number}')
    print(f'# Number of edges is {edges_number}')
    print(f'# in degrees are {in_degrees}')
    print(f'# out degrees are {out_degrees}')


if __name__ == '__main__':
    set_logging_config()
    build_graph_from_pickle_file()
