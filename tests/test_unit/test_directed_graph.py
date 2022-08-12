import os
from typing import List, Tuple, Dict
from unittest import TestCase
from unittest.mock import Mock, patch

from app.directed_graph import DirectedGraph
from app.exceptions import SerializedGraphFilePathNotFound, GraphNotBuiltExeption


class TestDirectedGraph(TestCase):

    def test_adjacency_list_build(self):
        # Given
        a_vertex_list: List[str] = ['a', 'b', 'c', 'c', 'd', 'e']
        an_edges_list: List[Tuple[str, str]] = [('a', 'b'), ('a', 'b'), ('d', 'c'), ('b', 'd'), ('a', 'd'), ('c', 'a'),
                                                ('b', 'b')]

        # When
        directed_graph = DirectedGraph()
        directed_graph.build_graph_from_vertices_and_edges(vertices_list=a_vertex_list, edges_list=an_edges_list)

        # Then
        expected_adjacency_list = {'a': ['b', 'b', 'd', ], 'b': ['d', 'b'], 'c': ['a'], 'd': ['c'], 'e': []}
        self.assertDictEqual(expected_adjacency_list, directed_graph.adjacency_list)

    def test_adjacency_list_build_when_not_valid_vertex_in_edge(self):
        # Given
        a_vertex_list: List[str] = ['a', 'b', 'c', 'c', 'd']
        an_edges_list: List[Tuple[str, str]] = [('a', 'b'), ('a', 'b'), ('d', 'c'), ('b', 'd'), ('a', 'd'), ('c', 'a'),
                                                ('b', 'e')]

        # When
        directed_graph = DirectedGraph()
        directed_graph.build_graph_from_vertices_and_edges(vertices_list=a_vertex_list, edges_list=an_edges_list)

        # Then
        expected_adjacency_list = {'a': ['b', 'b', 'd', ], 'b': ['d'], 'c': ['a'], 'd': ['c']}
        self.assertDictEqual(expected_adjacency_list, directed_graph.adjacency_list)

    def test_compute_number_of_vertices(self):
        # Given
        a_given_adjacency_list = {'a': ['b', 'b', 'd', ], 'b': ['d'], 'c': ['a'], 'd': ['c']}

        # When
        a_directed_graph = DirectedGraph()
        a_directed_graph.adjacency_list = a_given_adjacency_list
        computed_number_of_vertices = a_directed_graph.compute_number_of_vertices()

        # Then
        expected_number_of_vertices = 4
        self.assertEqual(expected_number_of_vertices, computed_number_of_vertices)

    def test_compute_number_of_edges(self):
        # Given
        a_given_adjacency_list = {'a': ['b', 'b', 'd', ], 'b': ['d'], 'c': ['a'], 'd': ['c']}

        # When
        a_directed_graph = DirectedGraph()
        a_directed_graph.adjacency_list = a_given_adjacency_list
        computed_number_of_edges = a_directed_graph.compute_number_of_edges()

        # Then
        expected_number_of_edges = 6
        self.assertEqual(expected_number_of_edges, computed_number_of_edges)

    def test_compute_out_degrees_per_vertex(self):
        # Given
        a_given_adjacency_list = {'a': ['b', 'b', 'd', ], 'b': ['d'], 'c': ['a'], 'd': ['c'], 'e': []}

        # When
        a_directed_graph = DirectedGraph()
        a_directed_graph.adjacency_list = a_given_adjacency_list
        computed_number_of_edges = a_directed_graph.compute_out_degrees_per_vertex()

        # Then
        expected_out_degrees: Dict[str, int] = {'a': 3, 'b': 1, 'c': 1, 'd': 1, 'e': 0}
        self.assertEqual(expected_out_degrees, computed_number_of_edges)

    def test_compute_in_degrees_per_vertex(self):
        # Given
        a_given_adjacency_list = {'a': ['b', 'b', 'd', ], 'b': ['d'], 'c': ['a'], 'd': ['c'], 'e': []}

        # When
        a_directed_graph = DirectedGraph()
        a_directed_graph.adjacency_list = a_given_adjacency_list
        computed_number_of_edges = a_directed_graph.compute_in_degrees_per_vertex()

        # Then
        expected_out_degrees: Dict[str, int] = {'a': 1, 'b': 2, 'c': 1, 'd': 2}
        self.assertEqual(expected_out_degrees, computed_number_of_edges)

    @patch('builtins.open')
    def test_deserialize_graph_should_raise_exception_when_file_not_found(self, mocked_open):
        # Given
        mocked_open.side_effect = FileNotFoundError
        provided_filepath = 'mysterious_file.pickle'

        # When
        a_directed_graph = DirectedGraph()
        with self.assertRaises(SerializedGraphFilePathNotFound) as custom_error:
            a_directed_graph.build_graph_from_pickle_file(provided_filepath)

        # Then
        mocked_open.assert_called_once_with(provided_filepath, 'rb')
        self.assertEqual(f'{provided_filepath} not found !', custom_error.exception.args[0])

    @patch('builtins.open')
    @patch('pickle.load')
    def test_deserialize_graph(self, mocked_pickle_load, mocked_open):
        # Given
        mocked_file = Mock()
        mocked_open.return_value = mocked_file
        mock_enter = Mock(return_value=(Mock(), None))
        mocked_open.return_value.__enter__ = mock_enter
        mocked_open.return_value.__exit__ = Mock(return_value=None)
        mocked_pickle_load.return_value = Mock()
        provided_filepath = 'directed_graph_file.pickle'
        a_directed_graph = DirectedGraph()

        # When
        a_directed_graph.build_graph_from_pickle_file(provided_filepath)

        # Then
        mocked_open.assert_called_once_with(provided_filepath, 'rb')
        mocked_pickle_load.assert_called_once_with(mock_enter.return_value)

    @patch('app.directed_graph.create_dir_if_not_exist')
    @patch('builtins.open')
    @patch('pickle.dump')
    @patch('time.strftime')
    def test_serialize_graph(self, mocked_strftime, mocked_pickle_dump, mocked_open, mocked_create_dir):
        # Given
        mocked_file = Mock()
        mocked_open.return_value = mocked_file
        mock_enter = Mock(return_value=(Mock(), None))
        mocked_open.return_value.__enter__ = mock_enter
        mocked_open.return_value.__exit__ = Mock(return_value=None)
        mocked_pickle_dump.return_value = Mock()
        mocked_strftime.return_value = '20220815-155045'
        a_given_adjacency_list = {'a': ['b', 'b', 'd', ], 'b': ['d'], 'c': ['a'], 'd': ['c'], 'e': []}
        provided_dir = 'a_directory'
        a_directed_graph = DirectedGraph()

        # When
        a_directed_graph.adjacency_list = a_given_adjacency_list
        a_directed_graph.serialize_graph(provided_dir)

        # Then
        mocked_create_dir.assert_called_once_with(provided_dir)
        mocked_open.assert_called_once_with(os.path.join(provided_dir, 'graph_20220815-155045.pickle', ), 'wb')
        mocked_pickle_dump.assert_called_once_with(a_given_adjacency_list, mock_enter.return_value)

    def test_serialize_empty_graph_should_raise_exception(self):
        # Given
        provided_dir = 'a_directory'

        # When
        a_directed_graph = DirectedGraph()
        with self.assertRaises(GraphNotBuiltExeption) as custom_error:
            a_directed_graph.serialize_graph(provided_dir)

        # Then
        self.assertEqual('You have to build a graph before serializing it!', custom_error.exception.args[0])