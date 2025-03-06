# classe de base
class Vertex:
    """
    représente les sommets et leurs adjacences dans un graphe
    
    on crée la classe qui s'occupe de toutes les adjacences entre 
    les sommets (vertex/vertices) et leurs autres sommets reliés
    les arrêtes (edges) ne sont pas représentés car c'est la matrice d'adjacence qui s'occupe de ça
    qui est situé dans la classe Graph
    """
    id = 0 # identifiant du sommet 

    def __init__(self, name:str, neighbor:list[V]=[]):
        self.name = name
        self.total_weight = sum([v.weight for v in neighbor]) # poids total du sommet
        self.neighbor = neighbor
        self.vertices_names = [v.name for v in self.neighbor]
        self.degree = len(neighbor)
        self.id = Vertex.id
        Vertex.id += 1

    def __str__(self):
        '''si on affiche Node (print(Node)) renverra ce qui suit'''
        res = f"{self.name} ["
        v_size = len(self.neighbor)
        for i, v in enumerate(self.neighbor):
            res += f"{v.name} w={v.weight}"
            if(i!=v_size-1):
                if v_size>1:
                    res+="," 
                res+=" "
        res+="]"
        return res
