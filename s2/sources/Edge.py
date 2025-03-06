class Edge:
    '''représente une arrête entre deux sommets/vertex
    manière différente de représenter un graphe'''

    id = 0
    
    def __init__(self, vfrom:str | int, vto:str | int, weight: int | float):
        self.a = vfrom
        self.b = vto
        self.weight = weight
        self.id = Edge.id
        Edge.id += 1
    
    def __eq__(self, other:"Edge"): # equivalent to self == other
        '''permet d'utiliser l'objet dans un set (le rendre hashable)
        pour faire des comparaisons entre des ensembles (set) d'objet Edge'''
        # On considère que deux arêtes sont égales si leurs sommets et poids sont égaux
        return (self.a == other.a and self.b == other.b and self.weight == other.weight)
    
    def __ne__(self, edge:object): # equivalent de !=
        return not self.__eq__(edge)    

    def __hash__(self): # equivalent to set(self) == set(other)
        """permet d'utiliser l'objet dans un set (le rendre hashable)
        pour faire des comparaisons entre des ensembles (set) d'objet Edge"""
        # Calculer le hash en fonction des attributs de l'objet
        return hash((self.start, self.end, self.weight))
