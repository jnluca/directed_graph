Annotations-storage
===================

## Introduction

Directed_graph is a application which allows to build a directed multigraph from a list of vertices and edges or from an
already serialized graph.

It can build an adjacency list from the inputs it receives. It can compute the number of edges and vertices and the
in degrees and out degrees of the vertices. Finally it can serialize the adjacency list to a pickle file.

We put ourselves in the case of a multigraph, in which we can have several edges between 2 vertices.

We are going represent the graph with an adjacency list because we want to be as efficient as possible during
serialization/deserialization activities. Adjacency matrices may be too sparse thus less efficient. Storing the edges
only or the edges and vertices would also lead to less compact outputs.

#### Installing dependencies

In order to run the application, you need first to install the appropriate conda environment with all dependencies.

```bash
$ ./setup_env.sh;
$ source activate directed_graph_challenge;
```

#### Setting up environment variables

There are no environment variables for this project

### Entrypoints

Entrypoints are located under `directed_graph/app/application`.

#### Create directed graph from list

The entrypoint `entry_point_create_directed_graph_from_list` creates a directed graph from a list of vertices and edges
which should be given as optional inputs. Default lists of inputs are given as examples.
When called, this entrypoint prints the characteristics of the graph and serializes it at `directed_graph/app/tmp`
into a file containing a timestamp.

It is assumed that the input are in string format. If they are complex objects, the properties
of the objects should be stored in a database and we would only use the id of these objects. An alternative to
that would be to create a vertex class and overwrite the `__repr__` method for instance. That method will be used
to identify the vertex in the adjacency list.

It is launched manually from the command line as follows :

```bash
$ python -m app.application.entry_point_create_directed_graph_from_list  --vertices-list a --vertices-list b --edges-list=a a --edges-list a b
```
Of course this entrypoint is to be called progammatically since it is not practical to enter the arguments manually.

#### Create directed graph from file

he entrypoint `entry_point_create_directed_graph_from_file` creates a directed graph from a file containing the serialization
of an already built graph.

It is launched as follows :

```bash
$ python -m app.application.entry_point_create_directed_graph_from_file  --filepath app/tmp/graph.pickle
```

#### Work on directed graph from file streaming

he entrypoint `entry_point_work_on_directed_graph_from_file_streaming` allows to compute the same statistics on the graph
as the other entry points, but without necessarily loading the full serialized file in memory in case
it is too big.

It is launched as follows :

```bash
$ python -m app.application.work_on_graph_from_pickle_file_streaming  --filepath app/tmp/graph.pickle
```

### Tests

This package contain the unit tests of the project.
