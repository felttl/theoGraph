# import packages
from random import randint


# import local classes
from Node import Node
from Graph import Graph

if __name__ == "__main__":
    # test sur un graphe connu (exo sur les graphe "village") avec sallin et tarjan

# Python program to create an undirected 
# graph and add nodes and edges to a graph



    graph = Graph([
        Node("a", ["c", "e"]),
        Node("b", ["c", "d", "i", "h"]),
        Node("c", ["a", "e", "b"]),
        Node("d", ["b", "e", "f"]),
        Node("e", ["a", "c", "d", "f"]),
        Node("f", ["e", "d", "i"]),
        Node("g", ["h", "i"]),
        Node("h", ["b", "g"]),
        Node("i", ["f", "b", "g"])   
    ])

    graph.render()


# end