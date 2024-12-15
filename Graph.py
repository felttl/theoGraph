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

        

# inheritance if oriented or not


# end