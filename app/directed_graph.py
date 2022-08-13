import os
import pickle
import time
from collections import Counter
from typing import List, Dict, Tuple

from app.config.logging_config import Logger
from app.exceptions import SerializedGraphFilePathNotFound, GraphNotBuiltException
from app.utils import create_dir_if_not_exist


class DirectedGraph:

    def __init__(self):
        self.adjacency_list: Dict[str, List[str]] = None
        self.logger = Logger(__class__.__name__).create()

    def build_graph_from_vertices_and_edges(self, vertices_list: List[str], edges_list: List[Tuple[str, str]]) -> None:
        self.adjacency_list = {vertex: [] for vertex in vertices_list}
        [self.adjacency_list[source].append(sink) for source, sink in edges_list if
         source in vertices_list and sink in vertices_list]
        self.logger.info('Created directed graph from list of vertices and edges')

    def build_graph_from_pickle_file(self, pickle_filepath: str) -> None:
        try:
            with open(pickle_filepath, 'rb') as in_file:
                self.adjacency_list = pickle.load(in_file)
                self.logger.info(f'Created directed graph from serialized adjacency list in  {pickle_filepath}')
        except FileNotFoundError:
            raise SerializedGraphFilePathNotFound(f'{pickle_filepath} not found !')

    def compute_number_of_vertices(self) -> int:
        if self.adjacency_list is None:
            raise GraphNotBuiltException('You have to build a graph before making computations on it!')
        return len(self.adjacency_list)

    def compute_number_of_edges(self) -> int:
        if self.adjacency_list is None:
            raise GraphNotBuiltException('You have to build a graph before making computations on it!')
        number_of_edges: int = 0
        for k in self.adjacency_list:
            number_of_edges += len(self.adjacency_list[k])
        return number_of_edges

    def compute_in_degrees_per_vertex(self) -> Dict[str, int]:
        if self.adjacency_list is None:
            raise GraphNotBuiltException('You have to build a graph before making computations on it!')
        list_of_sink_lists: List[List[str]] = list(self.adjacency_list.values())
        flat_list_of_sinks: List[str] = [item for sublist in list_of_sink_lists for item in sublist]
        in_degrees_counter: Dict[str, int] = dict(Counter(flat_list_of_sinks))
        in_degrees: Dict[str, int] = {k: (in_degrees_counter[k] if k in in_degrees_counter else 0) for k in
                                      self.adjacency_list}
        return in_degrees

    def compute_out_degrees_per_vertex(self) -> Dict[str, int]:
        if self.adjacency_list is None:
            raise GraphNotBuiltException('You have to build a graph before making computations on it!')
        return {k: len(self.adjacency_list[k]) for k in self.adjacency_list}

    def serialize_graph(self, dir_path: str) -> None:
        if self.adjacency_list is None:
            raise GraphNotBuiltException('You have to build a graph before serializing it!')
        create_dir_if_not_exist(dir_path)
        timestr: str = time.strftime("%Y%m%d-%H%M%S")
        with open(os.path.join(dir_path, 'graph_' + timestr + '.pickle'), 'wb') as out_file:
            pickle.dump(self.adjacency_list, out_file)
            self.logger.info(f'Serialized directed graph to {os.path.join(dir_path, "graph_" + timestr + ".pickle")}')

    def stream_compute_number_of_vertices(self, pickle_filepath: str) -> int:
        number_of_vertices: int = 0
        try:
            with open(pickle_filepath, 'rb') as in_file:
                while True:
                    try:
                        self.adjacency_list = pickle.load(in_file)
                        number_of_vertices += self.compute_number_of_vertices()
                    except EOFError:
                        break
                    else:
                        self.logger.info(f'Current number of vertices is {number_of_vertices}. Still reading data...')
                self.logger.info(f'Read the full graph. Final number of vertices is  {number_of_vertices}')
        except FileNotFoundError:
            raise SerializedGraphFilePathNotFound(f'{pickle_filepath} not found !')
        return number_of_vertices

    def stream_compute_number_of_edges(self, pickle_filepath: str) -> int:
        number_of_edges: int = 0
        try:
            with open(pickle_filepath, 'rb') as in_file:
                while True:
                    try:
                        self.adjacency_list = pickle.load(in_file)
                        number_of_edges += self.compute_number_of_edges()
                    except EOFError:
                        break
                    else:
                        self.logger.info(f'Current number of edges is {number_of_edges}. Still reading data...')
                self.logger.info(f'Read the full graph. Final number of edges is  {number_of_edges}')
        except FileNotFoundError:
            raise SerializedGraphFilePathNotFound(f'{pickle_filepath} not found !')
        return number_of_edges

    def stream_compute_in_degrees_per_vertex(self, pickle_filepath: str) -> Dict[str, int]:
        in_degrees: Dict[str, int] = Counter()
        try:
            with open(pickle_filepath, 'rb') as in_file:
                while True:
                    try:
                        self.adjacency_list = pickle.load(in_file)
                        in_degrees = Counter(self.compute_in_degrees_per_vertex()) + Counter(in_degrees)
                    except EOFError:
                        break
                    else:
                        self.logger.info('Still reading data...')
                self.logger.info('Read the full graph.')
        except FileNotFoundError:
            raise SerializedGraphFilePathNotFound(f'{pickle_filepath} not found !')
        return dict(in_degrees)

    def stream_compute_out_degrees_per_vertex(self, pickle_filepath: str) -> Dict[str, int]:
        out_degrees: Dict[str, int] = Counter()
        try:
            with open(pickle_filepath, 'rb') as in_file:
                while True:
                    try:
                        self.adjacency_list = pickle.load(in_file)
                        out_degrees = Counter(self.compute_out_degrees_per_vertex()) + Counter(out_degrees)
                    except EOFError:
                        break
                    else:
                        self.logger.info('Still reading data...')
                self.logger.info('Read the full graph.')
        except FileNotFoundError:
            raise SerializedGraphFilePathNotFound(f'{pickle_filepath} not found !')
        return dict(out_degrees)
