# import packages
from random import randint

# import local classes
from Node import Node
from Graph import Graph

if __name__ == "__main__":

    graph = Graph([
        Node("a", ["a", "b", "c", "d"]),
        Node("b", ["d", "c", "a"]),
        Node("c", ["a", "b", "d"]),
        Node("d", ["a", "c", "d"])
    ])

#    exit(0)
#    # nombre de couche horizontales
#    nb_layer = randint(1, 6)
#    # nombre de points par layer
#    layers = []
#    for i in range(nb_layer):
#        layers.append(randint(1, 5))
#    # construction des layers
#    names = [chr(layers[i]+65) if i < 26 else str(i%10) for i in range(sum(layers))]
#    nodes = []
#    for i in range(layers):
#        nodes.append([])
#        for j in range(layers[i]):
#            nodes[-1].append(Node(names[layers[i][j]]))



# end