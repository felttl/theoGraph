# from graphviz import Digraph # not compatible with macos
# from IPython import display # smooth lines
import networkx as netx
import matplotlib.pyplot as plt # for rendering

from Node import Node

class Graph:

    degree = 0

    def __init__(self, data:list[Node], format:str="json"):
        """nodes represents the tree itself 
        (''etc...'' : representes others nodes or elements added if necessary)        
        data format :
        [
            [master_node_1, [child_1, child_2, etc...]],
            [master_node_2, [child_1,child_2, etc... ]],
            etc...
        ]
        example : 
        [["a", ["b", "c", "d"]],["b", ["b", "c"]],["c", ["a", "b", "e"]]]
        """
        self.adj = []
        self.matr = []
        self.start = None
        self.end = None
        # no checking format
        for node in data:
            self.adj.append([node.name, node.vertex])
            Graph.degree += node.degree
        


    def represent():
        """show the graph as a image"""


    def add_start_end(self, s_name:str, e_name:str):
        """set the start adn the end"""
        self.start = s_name
        self.end = e_name

    def sallin()->[]:
        """alrogithme Sallin renvoyant """
        pass
    
    def tarjan()->[]:
        """algorithme de Tarjan"""
        pass

    def render(self):
        graph = netx.Graph()
        # create all graphic nodes
        for node in self.adj:
            graph.add_node(ord(node[0]))
        # joining nodes with edges 
        for node in self.adj:
            graph.add_edges_from([(node[0],e) for e in node[1]])

        #G = nx.complete_graph(5)
        #netx.draw(graph)  # networkx draw()

        netx.draw_networkx(graph)
        # plt.draw()  # pyplot draw()

    def _windows_render(self):
        """display th result as image (csv)"""
        digraph = Digraph()
        # create all graphic nodes
        for node in self.adj:
            digraph.node(node[0])
        # joining nodes with edges
        for node in self.adj:
            digraph.edges([node[0]+e for e in node[1]])

        # digraph # to render graphically
        # display.display_svg(digraph)
        digraph.view()
        

# inheritance if oriented or not


# end